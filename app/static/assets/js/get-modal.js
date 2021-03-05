$('#siteModal').on('show.bs.modal', function (e) {
  var href = '/deletar-produto/' + e.relatedTarget.id + '/';
  var h = e.relatedTarget.id

  $('#confirmar').attr('href', h);
});
