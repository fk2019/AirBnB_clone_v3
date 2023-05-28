document.addEventListener('DOMContentLoaded', () => {
  const url = 'http://127.0.0.1:5001/api/v1/status/';
  $.get(url, function (data) {
    if (data.status === 'OK') {
	    $('#api_status').addClass('available');
    } else {
	    $('#api_status').removeClass('available');
    }
  });
  const amenities = {};
  $('.popover').on('change', ':checkbox', function () {
    const am = $(this).data('id');
    if ($(this).is(':checked')) {
      amenities[am] = $(this).data('name');
    } else {
      delete amenities[am];
    }
    if (Object.keys(amenities).length > 0) {
      $('.amenities h4:eq(0)').text(Object.values(amenities).join(', '));
    //button filter
      $("button").on("click", (event) => {
        $.post({
          url: url2,
          data: JSON.stringify({"amenities": Object.keys(amenities)}),
          headers: { 'Content-Type': 'application/json' }
        }, handlePlaces);
      })
      // end button filter

    }

  });
  const url2 = 'http://127.0.0.1:5001/api/v1/places_search/';
  $.post({
    url: url2,
    data: JSON.stringify({}),
    headers: { 'Content-Type': 'application/json' }
  }, handlePlaces)

  function handlePlaces(data) {
    data.sort((a, b) => {
      const nameA = a.name.toUpperCase();
      const nameB = b.name.toUpperCase();
      if (nameA < nameB) {
        return -1;
      }
      if (nameA > nameB) {
        return 1;
      }
      return 0;
    });
    const section = $('.places');
    $.each(data, (i, place) => {
      const article = $('<article>');
      const headline = $('<div>').addClass('headline');
      const place_name = $('<h2>').text(place.name);
      const price = $('<div>').addClass('price_by_night').text('$' + place.price_by_night);
      headline.append(place_name).append(price);
      const info = $('<div>').addClass('information');
      const max_guest = $('<div>').addClass('max_guest');
      const guest_icon = $('<div>').addClass('guest_icon');
      const par = $('<p>').text(place.max_guest + ' Guests');
      max_guest.append(guest_icon).append(par);
      const number_rooms = $('<div>').addClass('number_rooms');
      const bed_icon = $('<div>').addClass('bed_icon');
      const room_par = $('<p>').text(place.number_rooms + ' Rooms');
      number_rooms.append(bed_icon).append(room_par);
      const number_bath = $('<div>').addClass('number_bathrooms');
      const bath_icon = $('<div>').addClass('bath_icon');
      const bath_par = $('<p>').text(place.number_bathrooms + ' Bathrooms');
      number_bath.append(bath_icon).append(bath_par);
      info.append(max_guest).append(number_rooms).append(number_bath);
      article.append(headline).append(info);
      const desc = $('<div>').addClass('description').html(place.description);
      const reviews = $('<div>').addClass('reviews');
      const review_h = $('<h2>').html(place.review.length + ' Reviews');
      const div = $('<div>');
      $.each(place.review, (i, review) => {
        const reviewer = $('<h3>');
        const ul = $('<ul>');
        const li = $('<li>');
        const rev_par = $('<p>');
        date = new Date(Date.parse(review.created_at));
        reviewer.text('From ' + review.name + ' the ' + date);
        rev_par.text(review.text);
        ul.append(li).append(rev_par);
        div.append(reviewer).append(ul);
      });
      reviews.append(review_h).append(div);
      desc.append(reviews);
      article.append(desc);
      section.append(article);
    });
  };



});
