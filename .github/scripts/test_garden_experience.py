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
            if width>=1200:
                assert await page.locator("#phg-desktop-links").is_visible()
                links=page.locator("#phg-desktop-links a")
                boxes=[await links.nth(i).bounding_box() for i in range(await links.count())]
                for a,b in zip(boxes,boxes[1:]):
                    assert a["x"]+a["width"]<=b["x"]+1,(width,"nav links overlap",a,b)
                assert boxes[-1]["x"]+boxes[-1]["width"]<=music["x"]+1,(width,"contact overlaps music")
                free=await page.locator("#phg-desktop-links .navCenterFree").bounding_box()
                assert abs(free["x"]+free["width"]/2-width/2)<4,(width,"free resources shifted")
            else: assert not await page.locator("#phg-desktop-links").is_visible()
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
            await page.wait_for_function("(n)=>document.querySelectorAll('#chat .bubble').length>=n",before+2)
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
        await page.locator("#navlinks .joinDrop").click()
        assert await page.locator("#modal.on").is_visible()
        assert not await page.locator("#navlinks").is_visible()
        await page.evaluate("closeModal();toggleMenu()")
        await page.locator("#navlinks .site-app-menu").click()
        assert await page.locator("#site-app-install-help").is_visible()
        print("PASS Join and Install actions")
        print("PAGE ERRORS",json.dumps(errors))
        assert not [e for e in errors if "site-experience" in e or "gardenNavigation" in e]
        await browser.close()
asyncio.run(main())
