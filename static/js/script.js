window.parseISOString = function parseISOString(s) {
  var b = s.split(/\D+/);
  return new Date(Date.UTC(b[0], --b[1], b[2], b[3], b[4], b[5], b[6]));
};

document.getElementById('venue-delete-btn').onclick = function(e) {
  const venue_id = e.target.dataset['id'];
  fetch('/venues/' + venue_id, {
    method: 'DELETE'
  })
  .then(function(response) {
    console.log(response.status);
    if (response.status == 200) {
      location.replace("/")
    } else {
      location.reload()
      $(window).scrollTop(0,0);
    }
  })
}