(function ($) {
	$(document).ready(function() {
		$('.slugify').each(function() {
			var autoslug = this.dataset.autoslug;
			$(this).slugify('input[name=' + autoslug + ']');
		});
	});
})(jQuery);
