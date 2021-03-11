$('#siteModal1').on('show.bs.modal', function (e) {
  var href = 'declarar-vendido/' + e.relatedTarget.id ;
  var h = e.relatedTarget.id

  $('#siteModal1  #confirmar').attr('href', h);
});
