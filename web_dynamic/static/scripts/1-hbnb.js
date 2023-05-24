document.addEventListener('DOMContentLoaded', () => {
  const amenity_ids = []
  $('#check_amenity input[type=checkbox]').on('click', (event) => {
	  let amenity_id = ''
    console.log($("input:checked").val())
	  /*if ($(this).is(':checked')) {
      console.log('clicked')
	    amenity_ids.push(amenity_id)
	  } else {
      console.log('Nooo')
	    const index = amenity_ids.indexOf(amenity_id)
	    if (index !== -1) {
		    amenity_ids.splice(index, 1)
	    }
    }*/
  })
})
