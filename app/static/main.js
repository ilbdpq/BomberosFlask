function tr_Seleccionar(tr_element) {
    const form_element = document.getElementById('abm');
    const td_elements = tr_element.querySelectorAll('td');
    const input_elements = form_element.querySelectorAll('input, select');

    td_elements.forEach((td_element, index) => {
        input_elements[index].value = td_element.textContent.trim();
    });
}

function form_Limpiar() {
    const form_element = document.getElementById('abm');
    const input_elements = form_element.querySelectorAll('input, select');

    input_elements.forEach((input_element) => {
        if (input_element.type != 'submit' && input_element.type != 'button') {
            if (input_element.tagName == 'SELECT') {
                input_element.selectedIndex = 0;
            }

            else if (input_element.tagName == 'INPUT') {
                input_element.value = "";
            }
        }
    });
}