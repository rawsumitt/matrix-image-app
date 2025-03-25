$(document).ready(function() {
    // Matrix Generation
    $('#matrixForm').submit(function(e) {
        e.preventDefault();
        const formData = $(this).serialize();
        
        $.ajax({
            url: '/generate_matrix',
            method: 'POST',
            data: formData,
            success: function(response) {
                $('#matrixResult').html(`<img src="${response.image_url}" alt="Generated Matrix">`);
            }
        });
    });

    // Image Upload
    $('#imageForm').submit(function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        $.ajax({
            url: '/upload_image',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                const images = response.paths.map(path => `<img src="${path}" alt="Processed Image">`).join('');
                $('#imageResult').html(images);
            }
        });
    });

    // Matrix Operations
    $('#operationForm').submit(function(e) {
        e.preventDefault();
        const formData = new FormData(this);
        
        $.ajax({
            url: '/matrix_operation',
            method: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function(response) {
                $('#operationResult').html(`<img src="${response.image_url}" alt="Operation Result">`);
            }
        });
    });
});
