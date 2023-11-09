document.addEventListener('DOMContentLoaded', function() {
    const buscador = document.getElementById('buscador');
    const listaProductos = document.getElementById('lista-productos');
    const transaccion = document.getElementById('transaccion');
    const finalizarBtn = document.getElementById('finalizar');
    const editarModalBtn = document.getElementById('editar-modal');

    let productoEditado = null;

    buscador.addEventListener('input', function() {
        const filtro = this.value.toLowerCase();

        for (const producto of listaProductos.children) {
            const nombre = producto.textContent.toLowerCase();

            if (nombre.includes(filtro)) {
                producto.style.display = 'block';
            } else {
                producto.style.display = 'none';
            }
        }
    });

    listaProductos.addEventListener('click', function(event) {
        const producto = event.target.closest('.producto');

        if (producto) {
            const nombre = producto.textContent.split(' - ')[0];
            const precio = parseFloat(producto.dataset.precio);

            const modalNombre = document.getElementById('modal-nombre');
            const modalPrecio = document.getElementById('modal-precio');
            const modalCantidad = document.getElementById('modal-cantidad');
            const agregarModalBtn = document.getElementById('agregar-modal');

            modalNombre.textContent = nombre;
            modalPrecio.textContent = `$${precio.toFixed(2)}`;
            modalCantidad.value = '1';
            editarModalBtn.style.display = 'none';
            agregarModalBtn.style.display = 'block';

            const modal = document.getElementById('modal');
            modal.style.display = 'block';

            agregarModalBtn.addEventListener('click', function() {
                const cantidad = parseInt(modalCantidad.value);
                const id = producto.dataset.id;

                let productoExistente = false;

                for (const item of transaccion.children) {
                    if (item.dataset.id === id) {
                        productoExistente = true;
                        break;
                    }
                }

                if (productoExistente && cantidad > 0) {
                    alert('Este producto ya está en la transacción.');
                } else if (cantidad > 0) {
                    const item = document.createElement('li');
                    item.dataset.id = id;
                    item.textContent = `${nombre} - $${precio.toFixed(2)} x ${cantidad}`;
                    transaccion.appendChild(item);

                    modal.style.display = 'none';
                    modalCantidad.value = '1';
                    calcularTotal();
                }
            });

            editarModalBtn.addEventListener('click', function() {
                if (productoEditado) {
                    const cantidad = parseInt(modalCantidad.value);

                    if (cantidad > 0) {
                        const id = productoEditado.dataset.id;
                        const nuevoNombre = modalNombre.textContent;
                        const nuevoPrecio = parseFloat(modalPrecio.textContent.substring(1));
                        productoEditado.textContent = `${nuevoNombre} - $${nuevoPrecio.toFixed(2)} x ${cantidad}`;
                        productoEditado.dataset.precio = nuevoPrecio;

                        modal.style.display = 'none';
                        modalCantidad.value = '1';
                        calcularTotal();
                        productoEditado = null;
                    }
                }
            });
        }
    });

    function calcularTotal() {
        const totalElement = document.getElementById('total');
        let total = 0;

        for (const item of transaccion.children) {
            const cantidad = parseInt(item.textContent.split(' x ')[1]);
            const precio = parseFloat(item.textContent.split(' x ')[0].split(' - ')[1].substring(1));
            total += precio * cantidad;
        }

        totalElement.textContent = `Total: $${total.toFixed(2)}`;
    }

    finalizarBtn.addEventListener('click', function() {
        const pagoElement = document.getElementById('pago');
        const pago = parseFloat(pagoElement.value);

        if (isNaN(pago)) {
            alert('Por favor, ingresa un monto válido.');
            return;
        }

        const totalElement = document.getElementById('total');
        const total = parseFloat(totalElement.textContent.split('$')[1]);

        if (pago < total) {
            alert('El monto en efectivo no es suficiente para cubrir la compra.');
            return;
        }

        const cambio = pago - total;
        alert(`Venta finalizada. El cambio es: $${cambio.toFixed(2)}`);
        transaccion.innerHTML = '';
        buscador.value = '';
        for (const producto of listaProductos.children) {
            producto.style.display = 'block';
        }
        totalElement.textContent = '';
        pagoElement.value = '';
    });

    const closeModal = document.querySelector('.close');
    closeModal.addEventListener('click', function() {
        const modal = document.getElementById('modal');
        modal.style.display = 'none';
    });

    // Habilitar la edición al hacer clic en un producto de la transacción
    transaccion.addEventListener('click', function(event) {
        const producto = event.target;

        if (producto && producto !== transaccion) {
            const cantidad = parseInt(producto.textContent.split(' x ')[1]);
            const precio = parseFloat(producto.textContent.split(' x ')[0].split(' - ')[1].substring(1));

            const modalNombre = document.getElementById('modal-nombre');
            const modalPrecio = document.getElementById('modal-precio');
            const modalCantidad = document.getElementById('modal-cantidad');
            const agregarModalBtn = document.getElementById('agregar-modal');

            modalNombre.textContent = producto.textContent.split(' x ')[0];
            modalPrecio.textContent = `$${precio.toFixed(2)}`;
            modalCantidad.value = cantidad;
            editarModalBtn.style.display = 'block';
            agregarModalBtn.style.display = 'none';

            const modal = document.getElementById('modal');
            modal.style.display = 'block';

            productoEditado = producto; // Guarda el producto que se está editando
        }
    });
});


