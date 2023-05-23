document.addEventListener('DOMContentLoaded', () => {
    const amenity_ids = []
    $(#check_amenity).on('change', () => {
	const amenity_id = $(this).data('id')
	if ($(this).is(':checked')) {
	    amenity_ids.push(amenity_id)
	} else {
	    const index = amenity_ids.indexOf(amenity_id)
	    if (index !== -1) {
		amenity_ids.splice(index, 1)
	}
    })
}
