$(document).ready(function() {
  var tableId = '.dormitory-basic'; // Jadvalning ID sini aniqlash

  // Serverdan ma'lumotlarni olish uchun AJAX so'rov yuborish
  $.ajax({
    url: '/api/dormitory-address/', // Serverdan ma'lumot olish uchun URL
    method: 'GET', // So'rov turi
    success: function(response) {
      // Ma'lumotlar muvaffaqiyatli olingan bo'lsa
      if ($(tableId).length) {
        $(tableId).DataTable({
          data: response, // Serverdan olingan ma'lumotlarni jadvalga kiritish
          columns: [
            { data: 'id', title: 'ID' },
            { data: 'name', title: 'Name' },
            { data: 'address', title: 'Address' },
            { data: 'description', title: 'Description' },
            { data: 'created_by', title: 'Created By' },
            // Qo'shimcha ustunlar kerak bo'lsa, shu yerga qo'shing
          ],
          columnDefs: [
            {
              targets: -1,
              title: 'Actions',
              orderable: false,
              searchable: false,
              render: function (data, type, full, meta) {
                return (
                  '<div class="d-inline-block">' +
                  '<a href="javascript:;" class="btn btn-sm btn-text-secondary rounded-pill btn-icon dropdown-toggle hide-arrow" data-bs-toggle="dropdown"><i class="ti ti-dots-vertical ti-md"></i></a>' +
                  '<ul class="dropdown-menu dropdown-menu-end m-0">' +
                  '<li><a href="javascript:;" class="dropdown-item">Details</a></li>' +
                  '<li><a href="javascript:;" class="dropdown-item">Archive</a></li>' +
                  '<div class="dropdown-divider"></div>' +
                  '<li><a href="javascript:;" class="dropdown-item text-danger delete-record">Delete</a></li>' +
                  '</ul>' +
                  '</div>' +
                  '<a href="javascript:;" class="btn btn-sm btn-text-secondary rounded-pill btn-icon item-edit"><i class="ti ti-pencil ti-md"></i></a>'
                );
              }
            }
          ],
          dom: '<"card-header flex-column flex-md-row"<"head-label text-center"><"dt-action-buttons text-end pt-6 pt-md-0"B>><"row"<"col-sm-12 col-md-6"l><"col-sm-12 col-md-6 d-flex justify-content-center justify-content-md-end mt-n6 mt-md-0"f>>t<"row"<"col-sm-12 col-md-6"i><"col-sm-12 col-md-6"p>>',
          displayLength: 7,
          lengthMenu: [7, 10, 25, 50, 75, 100],
          language: {
            paginate: {
              next: '<i class="ti ti-chevron-right ti-sm"></i>',
              previous: '<i class="ti ti-chevron-left ti-sm"></i>'
            }
          },
          buttons: [
            {
              extend: 'collection',
              className: 'btn btn-label-primary dropdown-toggle me-4 waves-effect waves-light border-none',
              text: '<i class="ti ti-file-export ti-xs me-sm-1"></i> <span class="d-none d-sm-inline-block">Export</span>',
              buttons: [
                {
                  extend: 'print',
                  text: '<i class="ti ti-printer me-1" ></i>Print',
                  className: 'dropdown-item',
                  exportOptions: {
                    columns: [0, 1, 2, 3, 4] // Export qilish uchun ustunlar
                  }
                },
                {
                  extend: 'csv',
                  text: '<i class="ti ti-file-text me-1" ></i>Csv',
                  className: 'dropdown-item',
                  exportOptions: {
                    columns: [0, 1, 2, 3, 4] // Export qilish uchun ustunlar
                  }
                },
                {
                  extend: 'excel',
                  text: '<i class="ti ti-file-spreadsheet me-1"></i>Excel',
                  className: 'dropdown-item',
                  exportOptions: {
                    columns: [0, 1, 2, 3, 4] // Export qilish uchun ustunlar
                  }
                },
                {
                  extend: 'pdf',
                  text: '<i class="ti ti-file-pdf me-1" ></i>Pdf',
                  className: 'dropdown-item',
                  exportOptions: {
                    columns: [0, 1, 2, 3, 4] // Export qilish uchun ustunlar
                  }
                }
              ]
            }
          ]
        });
      }
    },
    error: function(xhr, status, error) {
      console.error('Ma\'lumotlarni olishda xato:', error);
    }
  });
});
