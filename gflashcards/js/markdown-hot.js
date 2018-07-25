var img_regex = /(?:(?=^)|(?=\s).|^)([^\s<>"\']+\.(?:png|jpg|jpeg|gif))/g;
var markdownConverter = new showdown.Converter;

(function(Handsontable){
  function customRenderer(hotInstance, td, row, column, prop, value, cellProperties) {
    var text = Handsontable.helper.stringify(value);
    text = text.replace(/\n+/g, "\n\n");
    text = text.replace(img_regex,
      "<img src='$1' width=200 />");

    td.innerHTML = markdownConverter.makeHtml(text);

    return td;
  }

  // Register an alias
  Handsontable.renderers.registerRenderer('markdownRenderer', customRenderer);

})(Handsontable);
