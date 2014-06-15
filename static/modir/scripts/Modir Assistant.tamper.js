// ==UserScript==
// @name        Modir Assistant
// @namespace   http://modir.idehgostar.com/assistant/
// @description Assist Modir On Searching and Adding Tasks to Modir.Idehgostar.Com Project
// @version     2014.5.6
// @author      MeisamAhmadi
// @homepage    http://modir.idehgostar.com/assistant/
// @icon        http://localhost:12010/static/modir/images/assistant.ico
// @updateURL   http://localhost:12010/static/modir/scripts/Modir%20Assistant.tamper.js
// @downloadURL http://localhost:12010/static/modir/scripts/Modir%20Assistant.tamper.js
// @include     http://*/pages/task/view.html
// @exclude     http*//boards.4chan.org/*/catalog*
// @require		http://code.jquery.com/jquery-latest.js
// @grant       GM_getValue
// @grant       GM_setValue
// @grant       GM_xmlhttpRequest
// @grant       GM_openInTab
// @grant       GM_registerMenuCommand
// @grant       GM_setClipboard
// ==/UserScript==


static_server_address = "http://localhost:12010/static/modir/";

$('document').ready(function() {
    $.getScript(static_server_address+'scripts/assistant.js');
});
