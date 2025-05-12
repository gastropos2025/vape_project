document.addEventListener('DOMContentLoaded', function () {
    const carouselItems = document.querySelectorAll('.carousel-item');

    carouselItems.forEach(item => {
        item.addEventListener('click', function () {
            const saborId = this.getAttribute('data-sabor-id');
            fetch(`/sabor/${saborId}/productos/`)
                .then(response => response.json())
                .then(data => {
                    const productosContent = document.getElementById('productosContent');
                    productosContent.innerHTML = '';

                    if (data.productos.length === 0) {
                        productosContent.innerHTML += '<p>No hay productos disponibles para este sabor.</p>';
                    } else {
                        data.productos.forEach(producto => {
                            const formatoColombiano = new Intl.NumberFormat('es-CO', {
                                style: 'currency',
                                currency: 'COP',
                                minimumFractionDigits: 0,
                                maximumFractionDigits: 0
                            });
                            const precioFormateado = formatoColombiano.format(producto.precio);
                            const productoHTML = `
                                <div class="card mb-3">
                                    <div class="row g-0">
                                        <div class="col-md-4">
                                            ${producto.imagen ? `<img src="${producto.imagen}" class="img-fluid rounded-start" alt="${producto.nombre}">` : ''}
                                        </div>
                                        <div class="col-md-8">
                                            <div class="card-body">
                                                <h5 class="navbar-card-title">${producto.nombre}</h5>
                                                <br>
                                                <p class="flavor-item">${producto.informacion}</p>
                                                <br>
                                                <p class="card-text"><strong>Precio:</strong> ${precioFormateado}</p>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            `;
                            productosContent.innerHTML += productoHTML;
                        });
                    }

                    const saborHTML = `
                        <div class="card mb-3">
                            <div class="row g-0">
                                <div class="col-md-12">
                                    <div class="card-body">
                                        <div class="flavor-strain-container">
                                            <div class="flavor-section">
                                                <div class="flavor-label">FLAVOR</div>
                                                <div class="flavor-items">
                                                    ${data.sabor.sabor1 ? `<span class="flavor-item">${data.sabor.sabor1}</span>` : ''}
                                                    ${data.sabor.sabor2 ? `<span class="flavor-item">${data.sabor.sabor2}</span>` : ''}
                                                    ${data.sabor.sabor3 ? `<span class="flavor-item">${data.sabor.sabor3}</span>` : ''}
                                                </div>
                                            </div>
                                            <div class="strain-section">
                                                <div class="flavor-label">EFFECTS</div>
                                                <div class="flavor-item">${data.sabor.efecto}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    productosContent.innerHTML += saborHTML;

                    const modal = new bootstrap.Modal(document.getElementById('productosModal'));
                    modal.show();
                })
                .catch(error => console.error('Error:', error));
        });
    });
});