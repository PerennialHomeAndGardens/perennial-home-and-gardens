import asyncio, json, threading, http.server, socketserver
from pathlib import Path
from playwright.async_api import async_playwright
class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self,*args): pass
server=socketserver.TCPServer(("127.0.0.1",8765),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
async def main():
    async with async_playwright() as p:
        browser=await p.chromium.launch()
        page=await browser.new_page(viewport={"width":1440,"height":1000})
        await page.add_init_script("localStorage.setItem('phg_freebie_claimed','1');localStorage.setItem('phg_freebie_seen','1')")
        errors=[]
        page.on("pageerror",lambda e:errors.append(str(e)))
        await page.goto("http://127.0.0.1:8765",wait_until="load")
        await page.wait_for_selector("#phg-desktop-links",state="attached")
        await page.wait_for_function("typeof window.ask==='function' && document.querySelector('#music .phg-equalizer')")
        await page.evaluate("document.fonts.ready")
        for width in [1920,1440,1280,1200,1024,768,390,360]:
            await page.set_viewport_size({"width":width,"height":1000})
            music=await page.locator("#music").bounding_box()
            menu=await page.locator(".cleanMenu").bounding_box()
            assert abs(music["y"]-menu["y"])<3,(width,music,menu)
            assert music["x"]+music["width"]<=menu["x"]+1,(width,"icons overlap")
            assert menu["x"]+menu["width"]<=width,(width,"menu offscreen")
            assert not await page.locator(".newActions .site-app-button").count()
            assert not await page.locator("#phg-desktop-links").is_visible()
            assert await page.locator(".b20WoodBar .newActions").count()==1
            assert await page.locator("#music").evaluate("(n)=>getComputedStyle(n).borderTopWidth")=="0px"
            assert music["width"]==40 and menu["width"]==40
            await page.locator(".cleanMenu").click()
            assert await page.locator("#navlinks").is_visible()
            assert await page.locator("#navlinks .joinDrop").is_visible()
            assert await page.locator("#navlinks .site-app-menu").is_visible()
            assert await page.locator("#navlinks a").count()==9
            avatar=await page.locator(".assistantAvatar").bounding_box()
            await page.mouse.click(avatar["x"]+avatar["width"]/2,avatar["y"]+avatar["height"]/2)
            assert await page.locator("#ap").is_visible()
            assert not await page.locator("#navlinks").is_visible()
            await page.evaluate("toggleAssistant()")
            print("PASS responsive navigation",width)
        await page.set_viewport_size({"width":1440,"height":1000})
        await page.locator("#music").click()
        panel=page.locator("#site-shared-jukebox")
        await panel.wait_for(state="visible")
        assert await panel.locator(".x-dialog-heading img").count()==0
        assert await panel.get_by_text("InAct Entertainment LLC",exact=False).count()>0
        await panel.get_by_role("button",name="Movies",exact=True).click()
        assert await panel.get_by_role("heading",name="Movies, Trailers & Documentaries").count()==1
        assert await panel.locator(".x-track").count()==20
        text=await panel.inner_text()
        for old in ["Black Panther","Malcolm X","Moonlight","Selma","Black History"]: assert old not in text
        await panel.get_by_role("button",name="‹ Back",exact=True).click()
        await panel.get_by_role("link",name="Explore our free resources",exact=True).click()
        assert not await panel.is_visible()
        assert await page.locator("#free-resources").is_visible()
        print("PASS jukebox branding, 20 garden films, free-resource route")
        await page.evaluate("toggleAssistant()")
        kb=json.loads(Path("app-assets/tanya-knowledge.json").read_text())
        failed=[]
        for e in kb["entries"]:
            before=await page.locator("#chat .bubble").count()
            await page.evaluate("(q)=>{document.querySelector('#q').value=q;window.ask()}",e["question"])
            await page.wait_for_function("(n)=>document.querySelectorAll('#chat .bubble').length>=n",arg=before+2)
            answer=await page.locator("#chat .bubble").last.inner_text()
            if e["answer"] not in answer: failed.append({"question":e["question"],"expected":e["id"],"actual":answer[:180]})
        print("ANSWER MATCH FAILURES",json.dumps(failed))
        assert not failed,"Knowledge answers routed incorrectly"
        await page.evaluate("document.querySelector('#q').value='<img src=x onerror=alert(1)>';window.ask()")
        await page.wait_for_timeout(200)
        assert await page.locator("#chat img").count()==0
        await page.evaluate("document.querySelector('#q').value='Where can I park my spaceship?';window.ask()")
        await page.wait_for_timeout(200)
        assert "I need a little more detail" in await page.locator("#chat .bubble").last.inner_text()
        print("PASS 112 knowledge answers, safe text rendering, unknown question")
        await page.evaluate("toggleAssistant();toggleMenu()")
        target=await page.locator("#navlinks .joinDrop").bounding_box()
        await page.mouse.click(target["x"]+target["width"]/2,target["y"]+target["height"]/2)
        assert await page.locator("#modal.on").is_visible()
        assert not await page.locator("#navlinks").is_visible()
        await page.evaluate("closeModal();toggleMenu()")
        target=await page.locator("#navlinks .site-app-menu").bounding_box()
        await page.mouse.click(target["x"]+target["width"]/2,target["y"]+target["height"]/2)
        assert await page.locator("#site-app-install-help").is_visible()
        print("PASS Join and Install actions")
        print("PAGE ERRORS",json.dumps(errors))
        assert not [e for e in errors if "site-experience" in e or "gardenNavigation" in e]
        # Contact form: mobile uses one column, full-width fields and preserved message behavior.
        await page.set_viewport_size({"width":390,"height":844})
        
        if await page.locator("#navlinks").is_visible(): await page.evaluate("toggleMenu()")
        await page.evaluate("document.querySelector('#site-app-install-help')?.close()")
        await page.locator("#contact").scroll_into_view_if_needed()
        intro=await page.locator("#contact .contactGrid>div").bounding_box()
        form=await page.locator("#contact form").bounding_box()
        assert intro["y"]+intro["height"]<=form["y"],"Contact still side by side"
        assert form["width"]>300
        assert await page.locator("#cm").input_value()==""
        await page.locator("#cm").fill("Please help me plan a small garden.")
        await page.locator("#reason").select_option(label="Garden Coaching")
        assert await page.locator("#cm").input_value()=="Please help me plan a small garden."
        assert await page.locator("footer .footerLegal .site-app-footer-text").count()==1
        print("PASS contact stacking, readable fields, preserved message, compact footer")
        await page.goto("http://127.0.0.1:8765/tools/garden-calculator/",wait_until="load")
        await page.wait_for_selector(".phg-compact-header")
        assert await page.locator(".b20Logo img").evaluate("(n)=>n.complete && n.naturalWidth>0")
        await page.locator(".cleanMenu").click()
        assert await page.locator("#navlinks").is_visible()
        assert await page.locator('#navlinks a[href="/#contact"]').count()==1
        await page.locator(".cleanMenu").click()
        assert await page.locator(".result.show").count()>0
        await page.evaluate("scrollTo(0,600)")
        await page.wait_for_timeout(350)
        assert await page.locator(".b21StickyBrand").evaluate("(n)=>n.classList.contains('phg-header-away')")
        await page.evaluate("scrollTo(0,100)")
        await page.wait_for_timeout(350)
        assert not await page.locator(".b21StickyBrand").evaluate("(n)=>n.classList.contains('phg-header-away')")
        print("PASS standalone tool header, complete dropdown and scrolling")
        await page.goto("http://127.0.0.1:8765/reader-check.html")
        await page.wait_for_selector("body.ie-reader")
        for name in ["Comfort","Listen","Back to top"]:
            assert await page.get_by_role("button",name=name,exact=True).count()==1
        await page.get_by_role("button",name="Comfort",exact=True).click()
        assert await page.locator("#ie-comfort-panel").is_visible()
        print("COMFORT",await page.locator("#ie-comfort-panel").inner_text())
        await page.get_by_role("button",name="Lights on",exact=True).click()
        assert await page.locator("body").get_attribute("data-comfort-shade")=="on"
        await page.get_by_role("button",name="Lights off",exact=True).click()
        assert await page.locator("body").get_attribute("data-comfort-shade")=="off"
        await page.keyboard.press("Escape")
        await page.get_by_role("button",name="Listen",exact=True).click()
        assert await page.locator("#read-settings").is_visible()
        assert await page.locator("#read-rate").count()==1
        assert await page.locator("#read-stop").count()==1
        print("PASS Perennial reader toolbar controls")
        prompt=await browser.new_page()
        await prompt.clock.install()
        await prompt.goto("http://127.0.0.1:8765",wait_until="load")
        await prompt.wait_for_selector(".phg-compact-header")
        await prompt.clock.fast_forward(16000)
        print("PROMPT STATE",await prompt.evaluate("""()=>({hidden:document.hidden,resource:sessionStorage.getItem('phg-b3-resource-offer'),claimed:localStorage.getItem('phg_freebie_claimed'),opener:typeof window.openFreebie,busy:[...document.querySelectorAll('dialog[open],.modal.on,#ap.on,#navlinks.open')].map(n=>n.id),active:document.activeElement?.outerHTML.slice(0,200),app:[...document.querySelectorAll('.b17Preview')].filter(n=>{const r=n.getBoundingClientRect();return r.top<120&&r.bottom>innerHeight*.4}).map(n=>n.id)})"""))
        assert await prompt.locator("#freebieModal.on").is_visible()
        await prompt.evaluate("closeFreebie()")
        await prompt.clock.fast_forward(285000)
        assert await prompt.locator("#phg-tool-prompt").is_visible()
        assert not await prompt.locator("#freebieModal.on").is_visible()
        print("PASS 15-second resource offer and different five-minute tool offer")
        await browser.close()
asyncio.run(main())
