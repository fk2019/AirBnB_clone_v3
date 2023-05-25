document.addEventListener('DOMContentLoaded', () => {
  const amenities = {}
  $('input[type=checkbox]').on('change', function() {
    if ($(this).is(':checked')) {
      amenities[$(this).data('id')] = $(this).data('name')
    } else {
      delete amenities[$(this).data('id')]
    }
    if (Object.keys(amenities).length > 0) {
      $('.amenities h4:eq(0)').text(Object.values(amenities).join(', '))
    }
  })
})
