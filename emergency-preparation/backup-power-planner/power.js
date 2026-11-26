(() => {
  'use strict';

  const form = document.querySelector('#power-form');
  const rows = document.querySelector('#power-rows');
  const add = document.querySelector('#power-add');
  const inputMessage = document.querySelector('#power-input-message');
  const results = document.querySelector('#power-results');
  const storageMessage = document.querySelector('#power-storage');
  const station = [...form.querySelectorAll('.power-station input')];
  const storageKey = 'phg-backup-power-plan-v1';
  const maxDevices = 12;
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  const defaultStation = ['500', '100', '80', '', ''];
  const exampleDevices = [
    ['LED lamp', '8', '5', ''],
    ['Phone charger', '12', '2', ''],
    ['Wi-Fi router', '12', '8', ''],
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

    const remove = factory('button', 'Remove');
    remove.className = 'ep-plain-button';
    remove.type = 'button';
    remove.setAttribute('aria-label', 'Remove ' + (fields[0].value || 'device'));
    fields[0].addEventListener('input', () => {
      remove.setAttribute('aria-label', 'Remove ' + (fields[0].value.trim() || 'device'));
    });
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
    storageMessage.textContent = 'Browser storage is unavailable. Print the plan to keep your entries. Estimates assume no recharging.';
  }

  function savePlan(deviceFields) {
    try {
      localStorage.setItem(storageKey, JSON.stringify({
        station: station.map(field => field.value),
        devices: deviceFields.map(fields => fields.map(field => field.value)),
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

  function showRatings(active, running, continuous, surge) {
    const knownPeak = active.reduce((total, device) => total + (device.peak ?? device.watts), 0);
    const unknownPeaks = active.some(device => device.peak === null);
    const exceedsContinuous = Number.isFinite(continuous) && running > continuous;
    const exceedsSurge = Number.isFinite(surge) && knownPeak > surge;

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

  function update() {
    const deviceFields = readRows();
    savePlan(deviceFields);
    if (!form.checkValidity()) {
      showMessage('Check the station numbers and enter running watts and 0–24 daily hours for each device.');
      return;
    }

    const devices = deviceFields.map(([, watts, hours, peak]) => ({
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
  window.addEventListener('beforeprint', () => {
    form.querySelectorAll('.power-print-value').forEach(node => node.remove());
    for (const input of form.querySelectorAll('input')) {
      const value = factory('span', input.value || '—');
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
  form.hidden = false;
  update();
})();
