const
	DEFAULT_OPTIONS = {
		prefix: undefined,
		formSelector: '.formset-form',
		addContainer: '.formset-add-container',
		addButtonCreator: undefined,
		addButtonLabel: 'Add another',
		addButtonCssClass: 'btn btn-light',
		addCallback: undefined,
		addTitle: 'New item',
		deleteContainer: '.formset-delete-container',
		deleteButtonCreator: undefined,
		deleteButtonLabel: 'Delete item',
		deleteButtonCssClass: 'btn btn-xs-danger',
		deleteConfirmText: 'Are you sure? Item will be deleted after saving.',
		deleteCallback: undefined,
	},
	AVAILABLE_DATA_OPTIONS = {
		prefix: 'prefix',
		addButtonLabel: 'add-button-label',
		addTitle: 'add-title',
		addCallback: 'add-callback',
		deleteButtonLabel: 'delete-button-label',
		deleteConfirmText: 'delete-confirm-text',
		deleteCallback: 'delete-callback'
	},
	FORM_CHILD_ELEMENT_SELECTOR = 'input,select,textarea,label,div,a,span,img'
;


class FormsetInitializer {

	constructor(options) {
		document.querySelectorAll(options.selector).forEach(
			element => this.initialize(element));
	}

	initialize(element) {
		if (element.hasAttribute('data-formset-no-initialize')) {
			return;
		}

		new Formset(element, this.optionsForElement(element));
	}

	optionsForElement(element) {
		var options = {};

		Object.keys(AVAILABLE_DATA_OPTIONS).forEach(key => {
			var
				dataKey = 'data-formset-' + AVAILABLE_DATA_OPTIONS[key],
				value = element.getAttribute(dataKey)
			;
			if (value) {
				options[key] = value;
			}
		});

		if ('addCallback' in options) {
			options.addCallback = window[options.addCallback];
		}
		if ('deleteCallback' in options) {
			options.addCallback = window[options.deleteCallback];
		}

		return options;
	}
}


class FormsetForm {

	constructor(formset, element) {
		this.formset = formset;
		this.element = element;
	}

	get hasChildElements() {
		return this.element.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).length > 0;
	}

	updateIndex(newIndex) {
		this.element.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).forEach(
			element => this.updateElementIndex(element, newIndex));
	}

	updateElementIndex(element, newIndex) {
		var
			idLookup = new RegExp(this.formset.options.prefix + '-(\\d+|__prefix__)-'),
			idReplacement = this.formset.options.prefix + '-' + newIndex + '-'
		;

		['for', 'id', 'name'].forEach(field => {
			if (element.hasAttribute(field)) {
				element.setAttribute(
					field,
					element.getAttribute(field).replace(idLookup, idReplacement)
				);
			}
		});
	}

	createDeleteButton() {
		var button = document.createElement('button');
		button.innerText = this.formset.options.deleteButtonLabel;
		if (this.formset.options.deleteButtonCssClass) {
			button.setAttribute('class', this.formset.options.deleteButtonCssClass);
		}
		return button;
	}

	addDeleteButton() {
		var button = (
			this.formset.options.deleteButtonCreator ||
			this.createDeleteButton
		).call(this);

		if (this.formset.options.deleteContainer) {
			this.element.querySelector(
				this.formset.options.deleteContainer).appendChild(button);
		} else {
			this.element.appendChild(button);
		}

		button.addEventListener('click', this.deleteHandler.bind(this));
	}

	deleteHandler(event) {
		var
			deleteInput = this.element.querySelector('input[type=hidden][id$="-DELETE"]')
		;

		event.preventDefault();

		if (this.formset.options.deleteConfirmText) {
			if (!confirm(this.formset.options.deleteConfirmText)) {
				return false;
			}
		}

		if (deleteInput) {
			deleteInput.value = 'on';
			this.element.style.display = 'none';
		} else {
			this.formset.removeForm(this);
		}

		this.formset.ensureAddButtonVisibility();

		if (this.formset.options.deleteCallback) {
			this.formset.options.deleteCallback.call(this);
		}
	}

}


class Formset {

	constructor(element, options) {
		this.element = element;
		this.options = Object.assign({}, DEFAULT_OPTIONS, options);

		this.validateOptions();

		this.formTemplate = this.buildFormTemplate();

		this.totalFormsInput = this.element.querySelector(
			'#id_' + this.options.prefix + '-TOTAL_FORMS');
		this.maxFormsInput = this.element.querySelector(
			'#id_' + this.options.prefix + '-MAX_NUM_FORMS');

		this.initializeForms();

		this.addButton = this.addAddButton();
		this.ensureAddButtonVisibility();
	}

	validateOptions() {
		if (!this.options.prefix) {
			throw new Error('Prefix missing for formset.');
		}
		return true;
	}

	getFormElements() {
		return [...this.element.querySelectorAll(this.options.formSelector)];
	}

	initializeForms() {
		this.getFormElements().forEach((form) => {
			var formInstance = new FormsetForm(this, form);
			if (form.style.display !== 'none' && formInstance.hasChildElements) {
				formInstance.addDeleteButton();
			}
		});
	}

	removeForm(form) {
		form.element.remove();
		this.updateFormIndexes();
	}

	updateFormIndexes() {
		this.totalFormsInput.value = this.getFormElements().length;
		this.getFormElements().forEach((form, i) => {
			(new FormsetForm(this, form)).updateIndex(i);
		});
	}

	buildFormTemplate() {
		var
			template = this.getFormElements().pop().cloneNode(true),
			titleElement = template.querySelector('.formset-form-title'),
			deleteElement = template.querySelector('input[type=hidden][id$="-DELETE"]')
		;

		template.removeAttribute('id');
		template.classList.remove('existing');

		if (titleElement) {
			titleElement.innerText = this.options.addTitle;
		}

		if (deleteElement) {
			deleteElement.remove();
		}

		template.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).forEach(element => {
			var elementType = element.getAttribute('type');
			if (['checkbox', 'radio'].some(type => type === elementType)) {
				element.removeAttribute('checked');
			} else {
				element.value = '';
			}
		});

		return template;
	}

	ensureAddButtonVisibility() {
		var
			maxFormsValue = parseInt(this.maxFormsInput.getAttribute('value'), 10) || 0,
			totalFormsValue = this.getFormElements().filter(
				form => form.style.display !== 'none').length,
			visible = (maxFormsValue === 0 || (maxFormsValue - totalFormsValue > 0))
		;

		if (visible) {
			this.addButton.style.display = 'inherit';
		} else {
			this.addButton.style.display = 'none';
		}
	}

	createAddButton() {
		var button = document.createElement('button');
		button.innerText = this.options.addButtonLabel;
		if (this.options.addButtonCssClass) {
			button.setAttribute('class', this.options.addButtonCssClass);
		}
		return button;
	}

	addAddButton() {
		var button = (
			this.options.addButtonCreator ||
			this.createAddButton
		).call(this);


		if (this.options.addContainer) {
			this.element.querySelector(
				this.options.addContainer).appendChild(button);
		} else {
			this.element.appendChild(button);
		}

		button.addEventListener('click', this.addHandler.bind(this));
		return button;
	}

	addHandler(event) {
		event.preventDefault();

		var newForm = new FormsetForm(this, this.formTemplate.cloneNode(true));
		newForm.addDeleteButton();

		this.element.insertBefore(newForm.element, this.getFormElements().pop().nextSibling);
		this.updateFormIndexes();

		this.ensureAddButtonVisibility();

		if (this.options.addCallback) {
			this.options.addCallback.call(this);
		}
	}
}


export {Formset, FormsetInitializer};
