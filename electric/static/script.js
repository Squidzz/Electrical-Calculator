function addField() {
    const form = document.querySelector('form[action="/devices"]');
    const input = document.createElement('input');
    input.type = 'number';
    input.name = 'values';
    input.placeholder = 'Device Value';
    input.step = 'any';
    form.insertBefore(input, form.querySelector('button[type="submit"]'));
}
