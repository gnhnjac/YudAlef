
$(document).ready(function () {


    LoadPanel("center");

    ActivateStandaloneMode();

    if (typeof cefCustomObject !== 'undefined') {
      teacherRemarksManger.setupRemarks();
      $('body').addClass('teacher_remarks');
    }

    $(document).click(function (e) {
      //debugger;
      //debugger;
      if (e.target /*&& */) {

        if (
            ($(e.target).parents('.base .answers a').length == 1)
          ||
          ((e.target.nodeName == "A") && ($(e.target).parents('.base .answers').length == 1))
          ) {
          // a click on "a" element inside an answer area............ Ran this is for you :)
          //console.log("overriding onclick event a href to external url. href:" + e.target.href);
          //ShowExternalUrl('קישור בתשובה', e.target.href, 700, 700);
          //e.preventDefault ? e.preventDefault() : e.returnValue = false;
          //e.stopPropagation ? e.stopPropagation() : e.returnValue = false;
          //return false;
        }
      }
      var element = $(e.target);
      if (element.hasClass("asset_resize_link")) {
        if (!element.hasClass("enabled")) {
          var asset = $('#' + element.attr('data-id'));
          var modal = $('body').find('.modal[modal-id="' + element.attr('data-id') + '"]');
          element.addClass("enabled");
          
          modal.show();
        }
      }
    });
});
window.addEventListener('message', function (event) {
  try {
    var receivedData = JSON.parse(event.data);
    if (receivedData.action) {
      switch (receivedData.action) {
        case 'getMode':
          assetsApi_getMode(receivedData, event.source);
          break;
      }
    }
  } catch (e) { }
});
//assets
function assetsApi_sendMessage(data, source) {
  if (source) {
    var dataToSend = JSON.stringify(data);
    source.postMessage(dataToSend, '*');
  }
}
function assetsApi_getMode(data, source) {
  var result = { action: 'setMode', enable: false };
  assetsApi_sendMessage(result, source);
}
//end of assets

function UI() { }

function LoadPanel(type) {

    var panel = $(".base.panel." + type);
    var headH = $(".base.header").height() + 12;
    var winH = $(document).height();
    var panelH = winH - headH - 32;

    panel.show();
    $(".base.panel." + type + " .base.panelcontent").css("height", panelH);

    var title = $(".base.panel." + type + " > .paneltitle > .title");
    var text = $(".base.panel." + type + " > .panelcontent");
}

function ActivateStandaloneMode() {

    $(".base.pagetitle").unbind();
    $(".base.pagetitle").hover(function () {
        $(this).addClass("over");
    }, function () {
        $(this).removeClass("over");
    }).click(function () {
        var pageId = $(this).attr("pageid");
        $(".base.page[pageid=" + pageId + "]").toggle();
    });


    $(".base.multichoice .base.option").unbind("click").click(function (event) {
        event.preventDefault();
        event.stopPropagation();
        $(this).get(0).blur();
        return false;
    });

    $(".base.multichoice .base.option").each(function () {
        var item = $(this);
        if (item.attr("ischecked") == "true") {
            item.attr("checked", true); 
        }
    });


    $(".base.page").each(function (idx) {

        if ($(this).find(".base.questionmark.active").length > 0
            || $(this).find(".base.multichoice .base.option:checked").length > 0
            || has_selected_options(this)
            || true // open all answers (79655) 
        ) {
            $(".base.pagetitle[pageid=" + $(this).attr("pageid") + "]").addClass("active").next().addClass("display_answer");
        }
        if ($(this).find(".drag_zone").length > 0)
            $(this).before('<h1 class="drag_question"></h1>');
        $(this).find(".base.cz_select option[selected]")

    });
    ActivateAssetIframes();

}
function has_selected_options(obj) {
    if ($(obj).find(".base.cz_select option[selected]").length > 0) {
        for (i = 0; i < $(obj).find(".base.cz_select option[selected]").length; i++) {
            if ($(obj).find(".base.cz_select option[selected]")[i].getAttribute("id") != "0")
                return true;
        }
    }
    return false;
}

function ActivateAssetIframes() {

  $(".asset_resize_link").each(function (index) {
    var modal = $('body').find('.modal[modal-id="' + $(this).attr('data-id') + '"]');
    if ($('.modal').length == 0 || modal.length <= 0) {
      var asset = $('#' + $(this).attr('data-id'));
      var modal = $('\
				  <div class="modal" modal-id="' + $(this).attr('data-id') + '" style="position:fixed;top:0;left:0;z-index: 999999;">\
			      <span class="modal-close modal-close-x">X</span>\
			      <div class="modal-caption"></div>\
			      <div draggable="false" class="modal-content"></div>\
		      </div>\
       ');
      var ratio = false;
      var minH = 150;
      var minW = 150;
      var p_width = $(this).attr('modal-width');
      var p_height = $(this).attr('modal-height');
      if (typeof (p_width) != 'undefined' && typeof (p_height) != 'undefined') {
        ratio = p_width / p_height;
        modal.width(p_width + 'px');
        modal.height(p_height + 'px');
        minH = 0.1 * p_height;
        minW = 0.1 * p_width;
        if (minW < 150) {
          minW = 150;
        }
        if (minH < 150) {
          minH = 150;
        }
      }

      var title = ($(this).attr('modal-alt') != undefined) ? $(this).attr('modal-alt') : "&nbsp;";
      modal.find('.modal-caption').html(title)

      modal.find('.modal-close').click(function () {
        var data_id = modal.attr('modal-id');
        var cur_link = $('.asset_resize_link[data-id="' + modal.attr('modal-id') + '"]');
          cur_link.removeClass("enabled");
          modal.hide();        
      });
      $('body').append(modal);
      modal.draggable({ containment: "parent", handle: ".modal-caption", start: function () { $('body').append($(this)); } });
      modal.resizable({
        aspectRatio: ratio,
        minWidth: minW,
        minHeight: minH
      });
      var modalcontent = modal.find('.modal-content');
      asset.appendTo(modalcontent);
    }
  });
}



function NotSupported() {
    customAlert.Alert("תכונה זו לא נתמכת במצב בדיקת הבחינה");
}

function ShowExternalUrl() {
    NotSupported();
}
function ShowProtlab() {
    NotSupported();
}
function copyToClipboard(text) {
    var input = document.body.appendChild(document.createElement("input"));
    input.value = text;
    input.focus();
    input.select();
    document.execCommand('copy');
    input.parentNode.removeChild(input);
}
function OnExcelQuestionClick(obj) {
    let file = $(obj).attr("filename");
    let path = window.location.pathname;
    path = decodeURIComponent(path)
    path = path.substring(1, path.length);
    path = path.substring(0, path.lastIndexOf('/'));
    path = path + "/helpers/" + file;
    console.log(path)
    let alertText = " לא ניתן לפתוח את הקובץ דרך תוכנת המרבד." + "\n";
    alertText += "הנתיב הועתק וניתן להדביקו בשורת הכתובת של סייר הקבצים.";
    customAlert.Alert(alertText)
    copyToClipboard(path);
    }
function OnMuscoreQuestionClick(obj) {
  var path = "helpers/" + $(obj).attr("filename");

  document.location = path;
}
const customAlert = {
    init() {
        document.body.addEventListener("click", e => {
            if (e.target.classList.contains("custom-alert_exit")) {
                this.closeAlert(e.target);
            }
        });
    },
    //<button class="custom-alert__close custom-alert_exit material-icons">close</button>
    getHtmlTemplate(message) {
        return `
            <div class="custom-alert__overlay">
                <div class="custom-alert__window">
                    <div class="custom-alert__titlebar">
                    
                    <button class="custom-alert__close custom-alert_exit">X</button>
                    
                    <span class="custom-alert__title">שימו לב</span>
                    
                    </div>
                    <div class="custom-alert__content">
                    ${message}
                    <i class="material-icons md-48">warning</i>
                    </div>
                    
                    <button class="custom-alert__ok custom-alert_exit"> אישור</button>
                    
                </div>
            </div>
        `;
    },

    Alert(message = "הודעת ברירת מחדל") {

        const customAlertTemplate = this.getHtmlTemplate(message);
        document.body.insertAdjacentHTML("afterbegin", customAlertTemplate);
    },
    closeAlert(button) {
        let customAlertOverlay;
        if (button.classList.contains("custom-alert__close"))
            customAlertOverlay = button.parentElement.parentElement.parentElement;
        else {
            customAlertOverlay = button.parentElement.parentElement;
        }
        document.body.removeChild(customAlertOverlay);
    }
};

document.addEventListener("DOMContentLoaded", () => customAlert.init());





