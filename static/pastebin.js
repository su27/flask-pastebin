(function() {
  var global = this;

  var lib = global.pastebin = {
    urlRoot : '/',

    autoHideFlashes : function() {
      var flashes = $('p.flash:visible').hide();
      if (flashes.length) {
        flashes.slideDown('fast');
        window.setTimeout(function() {
          flashes.slideUp('slow');
        }, 5000);
      }
    },

    flash : function(message) {
      $('<p class=flash></p>')
        .append(message)
        .hide()
        .insertAfter('ul.nav')
        .slideDown('fast');
    },

    onNewReply : function(reply, type) {
      var pasteDescription = '';
      if (type == 'user') {
        pasteDescription = 'your paste <a href="' +
          pastebin.urlRoot + reply.paste_id + '">#' + reply.paste_id + '</a>';
      } else {
        pasteDescription = 'this paste';
      }
      var msg = $('<span>New reply to ' + pasteDescription + ': <a href="' +
        pastebin.urlRoot + reply.reply_id + '">#' + reply.reply_id + '</a></span>');
      if (reply.author)
        msg.append($('<span></span>').text(' ' + reply.author))
      lib.flash(msg);
    }

  };


  $(function() {
    /* animate the server side flashes a bit */
    lib.autoHideFlashes();
  });
})();
