(() => {
  'use strict';

  const form = document.querySelector('#power-form');
  const solarForm = document.querySelector('#solar-form');
  const forecastForm = document.querySelector('#forecast-form');
  const forecastFields = [...forecastForm.querySelectorAll('select')];
  const rows = document.querySelector('#power-rows');
  const add = document.querySelector('#power-add');
  const inputMessage = document.querySelector('#power-input-message');
  const results = document.querySelector('#power-results');
  const storageMessage = document.querySelector('#power-storage');
  const station = [...form.querySelectorAll('.power-station input')];
  const solar = [...solarForm.querySelectorAll('input')];
  const storageKey = 'phg-backup-power-plan-v1';
  const maxDevices = 12;
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  const defaultStation = ['500', '100', '80', '', ''];
  const exampleDevices = [
    ['LED lamp', '8', '5', ''],
    ['Phone charger', '12', '2', ''],
    ['Wi-Fi router', '12', '8', '', false],
  ];
  const specs = [
    { label: 'Device', type: 'text', maxLength: 55 },
    { label: 'Running watts (W)', type: 'number', min: 0.01, max: 100000, required: true },
    { label: 'Hours used per day', type: 'number', min: 0, max: 24, required: true },
    { label: 'Startup watts (W)', type: 'number', min: 0.01, max: 100000, placeholder: 'Optional' },
  ];

  function factory(tag, content) {
    const node = document.createElement(tag);
    if (content !== undefined) node.textContent = content;
    return node;
  }

  function updateAddButton() {
    add.disabled = rows.children.length >= maxDevices;
  }

  function addDevice(values = []) {
    const row = factory('div');
    row.className = 'power-row';
    const fields = specs.map((spec, index) => {
      const { label, ...attrs } = spec;
      const wrapper = factory('label', label);
      const input = factory('input');
      Object.assign(input, attrs, { value: typeof values[index] === 'string' ? values[index] : '' });
      if (input.type === 'number') input.step = 'any';
      wrapper.append(input);
      row.append(wrapper);
      return input;
    });

    const priority = factory('label', 'Keep on');
    priority.className = 'power-priority';
    const keep = factory('input');
    keep.type = 'checkbox';
    keep.checked = values[4] !== false;
    priority.append(keep);
    row.append(priority);

    const remove = factory('button', 'Remove');
    remove.className = 'ep-plain-button';
    remove.type = 'button';
    function labelControls() {
      const name = fields[0].value.trim() || 'device';
      remove.setAttribute('aria-label', 'Remove ' + name);
      keep.setAttribute('aria-label', 'Keep on ' + name);
    }
    labelControls();
    fields[0].addEventListener('input', labelControls);
    remove.addEventListener('click', () => {
      row.remove();
      updateAddButton();
      update();
      add.focus();
    });
    row.append(remove);
    rows.append(row);
    updateAddButton();
    return fields[0];
  }

  function loadPlan(stationValues, deviceValues) {
    for (const [index, input] of station.entries()) {
      const value = stationValues?.[index];
      input.value = typeof value === 'string' ? value : defaultStation[index];
    }
    rows.replaceChildren();
    deviceValues.slice(0, maxDevices).forEach(addDevice);
    updateAddButton();
  }

  function readRows() {
    return [...rows.children].map(row => [...row.querySelectorAll('input')]);
  }

  function useTemporaryStorageMessage() {
    storageMessage.textContent = 'Browser storage is unavailable. Print the plan to keep your entries. Runtime above assumes no recharging.';
  }

  function savePlan(deviceFields) {
    try {
      localStorage.setItem(storageKey, JSON.stringify({
        station: station.map(field => field.value),
        solar: solar.map(field => field.value),
        forecast: forecastFields.map(field => field.value),
        devices: deviceFields.map(fields => fields.map(field => field.type === 'checkbox' ? field.checked : field.value)),
      }));
    } catch {
      useTemporaryStorageMessage();
    }
  }

  function estimateText(value, unit) {
    return value > 0 && value < 0.01 ? 'Less than 0.01 ' + unit : 'About ' + number.format(value) + ' ' + unit;
  }

  function showMessage(message) {
    inputMessage.textContent = message;
    inputMessage.hidden = !message;
    results.hidden = Boolean(message);
  }

  function getRatings(active, running, continuous, surge) {
    const knownPeak = active.reduce((total, device) => total + (device.peak ?? device.watts), 0);
    const unknownPeaks = active.some(device => device.peak === null);
    const exceedsContinuous = Number.isFinite(continuous) && running > continuous;
    const exceedsSurge = Number.isFinite(surge) && knownPeak > surge;
    return { knownPeak, unknownPeaks, exceedsContinuous, exceedsSurge };
  }

  function showRatings(active, running, continuous, surge) {
    const { knownPeak, unknownPeaks, exceedsContinuous, exceedsSurge } =
      getRatings(active, running, continuous, surge);
    const continuousText = Number.isFinite(continuous)
      ? (exceedsContinuous ? ' This exceeds the continuous rating of ' : ' This is within the stated continuous rating of ') +
        number.format(continuous) + ' W.'
      : ' Enter your station’s continuous AC rating to compare.';
    document.querySelector('#power-running').textContent =
      'Running together: ' + number.format(running) + ' W.' + continuousText;

    const peakIntro = unknownPeaks ? 'Combined startup is at least ' : 'If all devices start together: ';
    const peakRating = Number.isFinite(surge)
      ? (exceedsSurge ? ' This exceeds the stated surge rating of ' :
        ' Stated surge rating: ') + number.format(surge) + ' W.'
      : ' Enter your station’s AC surge rating to compare.';
    document.querySelector('#power-startup').textContent = peakIntro + number.format(knownPeak) + ' W.' +
      peakRating + (unknownPeaks ? ' Some startup values are missing.' : '') +
      ' Check each outlet and the supported surge duration in the manual.';
    return exceedsContinuous || exceedsSurge;
  }

  function updateRuntime(deviceFields) {
    if (!form.checkValidity()) {
      showMessage('Check the station numbers and enter running watts and 0–24 daily hours for each device.');
      return;
    }

    const devices = deviceFields.map(([, watts, hours, peak, keep]) => ({
      keep: keep.checked,
      watts: watts.valueAsNumber,
      hours: hours.valueAsNumber,
      peak: peak.value === '' ? null : peak.valueAsNumber,
    }));
    if (devices.some(device => device.peak !== null && device.peak < device.watts)) {
      showMessage('Startup watts must be at least the running watts for that device.');
      return;
    }
    const active = devices.filter(device => device.hours > 0);
    if (!active.length) {
      showMessage('Add at least one device with daily hours above zero.');
      return;
    }

    const [capacity, charge, allowance, continuous, surge] = station.map(field => field.valueAsNumber);
    const available = capacity * (charge / 100) * (allowance / 100);
    const daily = active.reduce((total, device) => total + device.watts * device.hours, 0);
    const running = active.reduce((total, device) => total + device.watts, 0);
    showMessage('');
    const overload = showRatings(active, running, continuous, surge);

    document.querySelector('#power-available').value = estimateText(available, 'Wh');
    document.querySelector('#power-daily').value = estimateText(daily, 'Wh');
    document.querySelector('#power-days').value = estimateText(available / daily, 'days');
    document.querySelector('#power-hours').value = overload
      ? 'Combined load exceeds a rating'
      : estimateText(available / running, 'hours');
    const essentials = active.filter(device => device.keep);
    const essentialDaily = essentials.reduce((total, device) => total + device.watts * device.hours, 0);
    const essentialRunning = essentials.reduce((total, device) => total + device.watts, 0);
    const essentialRatings = getRatings(essentials, essentialRunning, continuous, surge);
    const essentialOverload = essentialRatings.exceedsContinuous || essentialRatings.exceedsSurge;
    return { daily, available, usableCapacity: capacity * (allowance / 100), overload, essentialDaily, essentialOverload };
  }

  function showSolarScenario(id, recharge, dailyLoad, usableAllowance) {
    document.querySelector('#solar-' + id + '-wh').value = estimateText(recharge, 'Wh');
    const summary = document.querySelector('#solar-' + id + '-offset');
    if (dailyLoad === undefined || !Number.isFinite(usableAllowance)) {
      summary.textContent = 'Complete the device schedule above to compare daily energy.';
      return;
    }
    const usable = recharge * usableAllowance / 100;
    const difference = usable - dailyLoad;
    const usableText = estimateText(usable, 'usable Wh') + '. ';
    if (Math.abs(difference) < 0.005) {
      summary.textContent = usableText + 'Matches the planned daily energy use.';
    } else {
      const gap = estimateText(Math.abs(difference), 'Wh');
      summary.textContent = usableText + (difference < 0
        ? gap + ' short of the daily plan.'
        : gap + ' above the daily plan.');
    }
  }

  function updateSolar(dailyLoad) {
    const [panel, limit, chargingAllowance, typical, low] = solar.map(field => field.valueAsNumber);
    const valid = solarForm.checkValidity();
    const message = document.querySelector('#solar-input-message');
    const problem = !valid ? 'Check the solar ratings, allowance, and peak-sun hours.' :
      low > typical ? 'Lower-sun hours must be at or below typical hours.' : '';
    message.textContent = problem;
    message.hidden = !problem;
    document.querySelector('#solar-results').hidden = Boolean(problem);
    if (problem) return;

    const chargingWatts = Math.min(panel, limit);
    const dailyFactor = chargingWatts * chargingAllowance / 100;
    const [capacityField, chargeField, allowanceField] = station;
    const usableAllowance = allowanceField.validity.valid ? allowanceField.valueAsNumber : NaN;
    document.querySelector('#solar-cap').textContent = panel > limit
      ? 'The estimate caps panel output at your station’s ' + number.format(limit) + ' W solar limit.'
      : 'The estimate starts with ' + number.format(chargingWatts) + ' W of rated panel power.';
    const recharge = { typical: dailyFactor * typical, low: dailyFactor * low, none: 0 };
    showSolarScenario('typical', recharge.typical, dailyLoad, usableAllowance);
    showSolarScenario('low', recharge.low, dailyLoad, usableAllowance);

    const headroom = document.querySelector('#solar-headroom');
    headroom.hidden = !capacityField.validity.valid || !chargeField.validity.valid;
    if (!headroom.hidden) {
      const room = capacityField.valueAsNumber * (100 - chargeField.valueAsNumber) / 100;
      headroom.textContent = room === 0
        ? 'At your starting charge, the battery is already full.'
        : 'At your starting charge, the battery has room for ' + number.format(room) +
          ' Wh before it fills, assuming no devices are running.';
    }

    return recharge;
  }

  function forecastDay(start, capacity, use, solarAvailable, chargeFirst) {
    const chargeAt = chargeFirst ? start : Math.max(0, start - use);
    const stored = Math.min(solarAvailable, Math.max(0, capacity - chargeAt));
    const availableForUse = chargeFirst ? start + stored : start;
    const covered = Math.min(use, availableForUse);
    return {
      stored,
      covered,
      shortfall: Math.max(0, use - covered),
      end: Math.max(0, start + stored - covered),
    };
  }

  function forecastSequence(runtime, recharge, daily) {
    const allowance = station[2].valueAsNumber / 100;
    const [first, second, third, timing] = forecastFields;
    const chargeFirst = timing.value === 'solar-first';
    let start = runtime.available;
    return [first, second, third].map(field => {
      const day = forecastDay(start, runtime.usableCapacity, daily, recharge[field.value] * allowance, chargeFirst);
      const entry = { start, ...day };
      start = day.end;
      return entry;
    });
  }

  function wattHours(value) {
    return value > 0 && value < 0.01 ? '<0.01 Wh' : number.format(value) + ' Wh';
  }

  function endCharge(value, capacity) {
    return number.format(100 * value / capacity) + '% · ' + wattHours(value);
  }

  function showShortfall(cell, value) {
    const hasShortfall = value > 1e-8;
    cell.textContent = hasShortfall ? wattHours(value) : 'None estimated';
    cell.classList.toggle('forecast-shortfall', hasShortfall);
  }

  function updateForecast(runtime, days) {
    const message = document.querySelector('#forecast-message');
    const result = document.querySelector('#forecast-results');
    message.hidden = Boolean(days);
    result.hidden = !message.hidden;
    if (result.hidden) {
      message.textContent = 'Complete the device schedule and solar settings above to see the forecast.';
      return;
    }

    const rows = document.querySelector('#forecast-days');
    const firstShortfall = days.findIndex(day => day.shortfall > 1e-8) + 1;
    rows.replaceChildren();

    days.forEach((day, index) => {
      const row = rows.insertRow();
      const heading = factory('th', 'Day ' + (index + 1));
      heading.scope = 'row';
      row.append(heading);
      row.insertCell().textContent = wattHours(day.start);
      row.insertCell().textContent = wattHours(day.stored);
      row.insertCell().textContent = wattHours(day.covered);
      showShortfall(row.insertCell(), day.shortfall);
      row.insertCell().textContent = endCharge(day.end, runtime.usableCapacity);
    });

    let summary = firstShortfall
      ? 'The first estimated shortfall is on Day ' + firstShortfall + '.'
      : 'The model covers the planned energy use on all three days.';
    if (runtime.overload) summary += ' A combined load still exceeds a rating you entered above.';
    document.querySelector('#forecast-summary').textContent = summary;
  }

  function updateEssentials(runtime, recharge, fullDays) {
    const message = document.querySelector('#essentials-message');
    const result = document.querySelector('#essentials-results');
    message.hidden = Boolean(runtime?.essentialDaily);
    result.hidden = !message.hidden;
    if (result.hidden) {
      message.textContent = runtime
        ? 'Mark at least one device with daily use to keep on in the essentials plan.'
        : 'Complete the battery and device schedule above to compare the two plans.';
      return;
    }

    const fullRuntime = runtime.available / runtime.daily;
    const essentialRuntime = runtime.available / runtime.essentialDaily;
    const savings = runtime.daily - runtime.essentialDaily;
    document.querySelector('#essentials-full-runtime').value = estimateText(fullRuntime, 'days');
    document.querySelector('#essentials-runtime').value = estimateText(essentialRuntime, 'days');
    document.querySelector('#essentials-full-daily').textContent = wattHours(runtime.daily) + ' per day';
    document.querySelector('#essentials-daily').textContent = wattHours(runtime.essentialDaily) + ' per day';
    const extraRuntime = runtime.available > 0
      ? ' and adds ' + estimateText(essentialRuntime - fullRuntime, 'days').toLowerCase() + ' on the starting charge'
      : '';
    document.querySelector('#essentials-savings').textContent = savings > 1e-8
      ? 'Pausing the other devices saves ' + wattHours(savings) + ' per day' + extraRuntime + '.'
      : 'Both plans currently use the same amount of energy.';
    const notices = [];
    if (runtime.overload) notices.push('The full schedule exceeds a combined power rating.');
    if (runtime.essentialOverload) notices.push('Essentials only also exceeds a combined power rating.');
    const ratings = document.querySelector('#essentials-ratings');
    ratings.hidden = notices.length === 0;
    ratings.textContent = notices.join(' ');

    const table = document.querySelector('#essentials-forecast-table');
    const forecastMessage = document.querySelector('#essentials-forecast-message');
    table.hidden = !recharge;
    forecastMessage.hidden = Boolean(recharge);
    if (!recharge) return;

    const body = document.querySelector('#essentials-days');
    body.replaceChildren();
    forecastSequence(runtime, recharge, runtime.essentialDaily).forEach((day, index) => {
      const row = body.insertRow();
      const heading = factory('th', 'Day ' + (index + 1));
      heading.scope = 'row';
      row.append(heading);
      row.insertCell().textContent = endCharge(fullDays[index].end, runtime.usableCapacity);
      showShortfall(row.insertCell(), fullDays[index].shortfall);
      row.insertCell().textContent = endCharge(day.end, runtime.usableCapacity);
      showShortfall(row.insertCell(), day.shortfall);
    });
  }

  function update() {
    const deviceFields = readRows();
    savePlan(deviceFields);
    const runtime = updateRuntime(deviceFields);
    const recharge = updateSolar(runtime?.daily);
    const days = runtime && recharge ? forecastSequence(runtime, recharge, runtime.daily) : null;
    updateForecast(runtime, days);
    updateEssentials(runtime, recharge, days);
  }

  add.addEventListener('click', () => {
    addDevice().focus();
    update();
  });
  document.querySelector('#power-example').addEventListener('click', () => {
    loadPlan(defaultStation, exampleDevices);
    update();
  });
  form.addEventListener('input', update);
  form.addEventListener('submit', event => event.preventDefault());
  solarForm.addEventListener('input', update);
  solarForm.addEventListener('submit', event => event.preventDefault());
  forecastForm.addEventListener('change', update);
  forecastForm.addEventListener('submit', event => event.preventDefault());
  window.addEventListener('beforeprint', () => {
    document.querySelectorAll('.power-print-value').forEach(node => node.remove());
    for (const input of [...form.querySelectorAll('input'), ...solar, ...forecastFields]) {
      const printable = input.type === 'checkbox'
        ? (input.checked ? 'Yes' : 'No')
        : input.selectedOptions?.[0]?.textContent || input.value || '—';
      const value = factory('span', printable);
      value.className = 'power-print-value';
      input.after(value);
    }
  });

  let saved;
  try {
    saved = JSON.parse(localStorage.getItem(storageKey) || 'null');
  } catch {
    useTemporaryStorageMessage();
  }
  const validDevices = Array.isArray(saved?.devices) && saved.devices.every(Array.isArray);
  loadPlan(saved?.station, validDevices ? saved.devices : exampleDevices);
  for (const [index, input] of solar.entries()) {
    const remembered = saved?.solar?.[index];
    if (typeof remembered === 'string') input.value = remembered;
  }
  for (const [index, field] of forecastFields.entries()) {
    const remembered = saved?.forecast?.[index];
    if ([...field.options].some(option => option.value === remembered)) field.value = remembered;
  }
  form.hidden = false;
  solarForm.hidden = false;
  forecastForm.hidden = false;
  update();
})();
