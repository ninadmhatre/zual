toastr.options = {
  "closeButton": false,
  "debug": false,
  "newestOnTop": true,
  "progressBar": false,
  "positionClass": "toast-top-right",
  "preventDuplicates": true,
  "onclick": null,
  "showDuration": "300",
  "hideDuration": "1000",
  "timeOut": "5000",
  "extendedTimeOut": "1000",
  "showEasing": "swing",
  "hideEasing": "linear",
  "showMethod": "fadeIn",
  "hideMethod": "fadeOut"
}

var flashToToaster = function() {
    $('.flash-msg').each(function() {
        alert($(this).val());
    });
};

var showInfo = function(msg) { toastr.info(msg); };
var showError = function(msg) { toastr.error(msg); };
var showSuccess = function(msg) { toastr.success(msg); };

var toggleButton = function(btnType, enable) {
    var $btn = $('input[type="' + btnType +'"]');
    if (enable) {
        $btn.attr('disabled', false);
    } else {
        $btn.attr('disabled', true);
    }
};

var enableButton = function(btnType) {
    toggleButton(btnType, true);
};

var disableButton = function(btnType) {
    toggleButton(btnType, false);
};
