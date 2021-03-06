/* Feedback form automation */
$(function() {
	/* append error notification */
	var append_error_info = function(selection, msg, klass=null) {
		selection.each(function() {
			var icon = $('<span class="' + (klass||'') + ' label label-danger"><span class="glyphicon glyphicon-alert"></span></span>');
			icon.tooltip({ title: msg });
			$(this).append(icon);
		});
	};

	/* append done notification */
	var append_done_info = function(selection, msg, klass=null) {
		selection.each(function() {
			var icon = $('<span class="' + (klass||'') + ' label label-success"><span class="glyphicon glyphicon-ok "></span></span>');
			icon.tooltip({ title: msg });
			$(this).append(icon);
		});
	};

	/* update things when something in form has changed */
	var form_changed = function() {
		var form = $(this);
		var sts = $('#' + form.data('state-id'));
		var panel = form.closest('.response-panel');
		var changed = false;
		form.find('textarea').each(function() {
			changed = this.value != this.defaultValue;
			return !changed;
		});
		if (changed) {
			sts.removeClass(sts.data('orig-style'));
			sts.addClass('label-default');
			sts.text('not saved');
			panel.find('.response-by').hide();
			panel.find('.reset-button').show();
		} else {
			sts.removeClass('label-default');
			sts.addClass(sts.data('orig-style'));
			sts.text(sts.data('orig-text'));
			panel.find('.reset-button').hide();
			panel.find('.response-by').show();
		}
	};

	/* react to edit in textarea */
	var on_textarea_change = function() {
		$(this).closest('form').each(function() { form_changed.call(this); });
	};

	/* Buttons that replace radio select */
	var on_submit_button = function(e) {
		e.preventDefault();
		var button = $(this);
		var radio = $(button.data('radio'));
		radio.prop('checked', true);
		button.closest('.buttons-for-radio').find('.btn.active').removeClass('active');
		button.addClass('active');
		button.closest('form').submit();
	}
	var replace_with_buttons = function() {
		var src = $(this);
		// create new form-group and select it
		var dst = src.after('<div class="form-group buttons-for-radio"><div class="col-xs-12"><div class="btn-group btn-group-justified" role="group"></div></div></div>').next();
		var cont = dst.find('.btn-group');
		// for every input radio, create new button
		src.find('input[type="radio"]').each(function() {
			var radio_pure = this;
			var radio = $(this);
			var text = radio.parent().text();
			var color = radio.data('color');
			if (radio.prop('disabled')) {
				cont.append('<div class="btn-group" role="group"></div>')
			} else {
				cont.append('<div class="btn-group" rule="group"><button class="btn btn-' +
					color + '">' + text + '</button></div>');
				var button = cont.find('button').last();
				button.data('radio', radio_pure).on('click', on_submit_button);
				if (radio.is(':checked'))
					button.addClass('active');
			}
		});
		// hide original form-group
		src.hide();
	};
;

	/* hook reset button to also hide itself and update form state */
	var on_reset_button = function() {
		var me = $(this);
		$('#' + me.data('form-id')).each(function() {
			this.reset();
			form_changed.call(this);
		});
	};

	/* disable respone panel */
	var show_noedit_overlay = function() {
		var overlay = $(this).find('.overlay');
		overlay.show();
		overlay.find('button.edit-btn').on('click', function() {
			overlay.hide();
		});
	};

	/* clear status tags from response form */
	var clear_status_tags = function(panel) {
		panel.find(".panel-heading .status-tag").remove();
	};

	/* add status tag to response form */
	var add_status_tag = function(panel, text, color) {
		var html = '<span class="status-tag label label-' + color + ' pull-right">' + text + '</span>';
		panel.find(".panel-heading").append(html);
	};

	/* use ajax to post forms */
	var ajax_submit = function(e) {
		e.preventDefault();
		var me = $(this);
		var url = this.action;
		var post_data = me.serialize();
		var panel_id = '#' + me.data('panel-id');
		var panel = $(panel_id);
		clear_status_tags(panel);
		add_status_tag(panel, "Sending...", "default");

		$.ajax({
			type: 'POST',
			url: url,
			data: post_data,
			success: function(data, textStatus, xhr) {
				console.log("Post to '" + url + "' with data '" + post_data + "'");
				var panel = $(panel_id);
				var new_panel = $(data).find(panel_id);
				if (new_panel.length > 0) {
					// update form
					$(panel_id).replaceWith(new_panel);
					panel = $(panel_id);
					on_form_insert(panel);
					if (xhr.status == 201) {
						// submission was ok
						console.log(" -> was good");
						add_status_tag(panel, "Saved", "success");
						new_panel.each(show_noedit_overlay);
					} else {
						console.log(" -> had errors");
						add_status_tag(panel, "Not saved", "warning");
						add_status_tag(panel, "Has errors", "danger");
					}
				} else {
					// Probably login form...
					console.log(
						" -> Got response with status 200 and content" +
						" that doesn't have panel with id '" + panel_id +
						"'. data was '" + data +
						"'");
					clear_status_tags(panel);
					add_status_tag(panel, "Not saved", "warning");
					add_status_tag(panel, "Unknown error", "danger");
					alert("Unknown error occured. See javascript console!");
				}
			},
			timeout: 10000,
			error: function(xhr, textStatus, error) {
				clear_status_tags(panel);
				add_status_tag($(panel_id), "Not saved", "warning");
				if (textStatus == "timeout") {
					// act on timeout
					add_status_tag($(panel_id), "Update timeouted!", "danger");
				} else if (xhr.status == 403) {
					// no authentication
					add_status_tag($(panel_id), "Not authenticated!", "danger");
					alert("You are not authenticated. Do that in another tab, then open this reponse in another tab and copy input. Then you can refesh this page.");
					$(panel_id + ' .panel-footer').html('<a href="'+url+'">Link to this responses update page. Open in new tab!</a>');
				} else {
					// axt on other errors: xhr.status
					add_status_tag($(panel_id), "Server returned " + xhr.status, "danger");
				}
			},
		});
	};

	/* color tags */
	var ajax_set_tag_state = function() {
		var me = $(this);
		var container = me.parent();
		var errorname = 'error-' + me.data('tagpk');
		var active = me.hasClass('colortag-active');
		// first, make change
		if (active) me.removeClass('colortag-active');
		else me.addClass('colortag-active');
		// get previous or new defer object
		var defer = container.data('rlock') || $.when();
		// connect to defer chain
		container.data('rlock', defer.then(function() {
			var spinner = $('<span class="updating glyphicon glyphicon-refresh gly-spin"></span>');
			container.find('.uploadok, .'+errorname).remove(); // clear old done and error notifications
			container.append(spinner); // add spinner
			var promise = $.Deferred(); // this promise is fulfilled when ajax request is completed, thus we get serialized updates per response
			$.ajax({
				type: active ? 'DELETE' : 'PUT',
				url: me.data('tagurl'),
				timeout: 10000,
				success: function(data, textStatus, xhr) {
					append_done_info(container, "Update of '" + me.text() + "' ok.", 'uploadok');
				},
				error: function(xhr, textStatus, error) {
					// if there was error, revert change
					if (active) me.addClass('colortag-active');
					else me.removeClass('colortag-active');
					// display and log error
					var name = me.text();
					append_error_info(container, (textStatus == 'timeout') ?
						( "Update of '" + name + "' timeouted." ) :
						( "Update of '" + name + "' failed. Server returned " + xhr.status + ". Check js/server logs." ),
						errorname
					);
					console.log("Tag update failed '" + textStatus + "' return code " + xhr.status + " with data: " + xhr.responseText);
				},
				complete: function() {
					spinner.remove(); // remove spinner
					promise.resolve(); // always resolve promise, no failures
				},
			});
			return promise;
		}));
	}


	/* call for inserted forms */
	var on_form_insert = function(dom=null) {
		if (dom === null) {
			dom = $(document);
		}

		dom.find('form.ajax-form').submit(ajax_submit);
		dom.find('textarea.track-change').on('change keyup paste', on_textarea_change);
		dom.find('.reset-button[data-form-id]').on('click', on_reset_button);
		dom.find('[data-toggle="tooltip"]').tooltip();
		dom.find('.replace-with-buttons').each(replace_with_buttons);
		dom.find('.response-panel.disabled').each(show_noedit_overlay);
		dom.find('.colortag').on('click', ajax_set_tag_state);
	};

	/* on page load forms got inserted */
	on_form_insert();

	/* setup jquery ajax with csrf token */
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			var csrftoken = Cookies.get('csrftoken');
			if (!this.crossDomain && csrftoken) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});
});

