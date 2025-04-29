function getLastId() {
    let inputs = document.querySelectorAll('input[name^="nw_"]');
    if (inputs.length === 0) return 0;

    let value = inputs[inputs.length - 1].getAttribute('name');
    lastNum = parseInt(value.replace('nw_', ''));
    return isNaN(lastNum) ? 0 : lastNum
}


function countNwElements() {
    let inputs = document.querySelectorAll('input[name^="nw_"]');
    return inputs.length;
}

function createNewRow(template, container) {
    const newRow = document.importNode(template, true);
    lastId = getLastId()
    word = newRow.getElementById("new-word")
    word.name = `nw_${lastId + 1}`
    transl = newRow.getElementById("new-translation")
    transl.name = `nt_${lastId + 1}`
    container.append(newRow)
}

document.addEventListener('DOMContentLoaded', () => {
    const addButton = document.getElementById("add-row");
    const container = document.getElementById("words-container");
    const template = document.getElementById("row-template").content;

    if (getLastId() === 0) {
        for (let i = 0; i < 2; i++) {
            createNewRow(template, container)
        }
    }

    // adding new row
    addButton.addEventListener('click', () => {
        createNewRow(template, container)
    });

    // delete row
    container.addEventListener('click', (e) => {
        if (e.target.closest('.remove-input-group')) {
            const rowToDelete = e.target.closest('.input-group');
            rowToDelete.classList.add('removing');
            setTimeout(() => rowToDelete.remove(), 300)
        }
    });
});
