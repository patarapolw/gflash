var img_regex = /([^\s<>"\']+\.(?:png|jpg|jpeg|gif))/g;

(function(Handsontable){
  function customRenderer(hotInstance, td, row, column, prop, value, cellProperties) {
    var text = Handsontable.helper.stringify(value);
    text = text.replace(/\n+/g, "\n\n");
    text = text.replace(img_regex,
      "<img src='$1' width=200 />");

    var converter = new showdown.Converter;
    td.innerHTML = converter.makeHtml(text);

    return td;
  }

  // Register an alias
  Handsontable.renderers.registerRenderer('markdownRenderer', customRenderer);

})(Handsontable);
