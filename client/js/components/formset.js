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
  }
const AVAILABLE_DATA_OPTIONS = {
  prefix: 'prefix',
  addButtonLabel: 'add-button-label',
  addTitle: 'add-title',
  addCallback: 'add-callback',
  deleteButtonLabel: 'delete-button-label',
  deleteConfirmText: 'delete-confirm-text',
  deleteCallback: 'delete-callback',
}
const FORM_CHILD_ELEMENT_SELECTOR = 'input,select,textarea,label,div,a,span,img'

class FormsetForm {
  constructor(formset, element) {
    this.formset = formset
    this.element = element
  }

  get hasChildElements() {
    return this.element.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).length > 0
  }

  updateIndex(newIndex) {
    this.element.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).forEach(
      (element) => this.updateElementIndex(element, newIndex),
    )
  }

  updateElementIndex(element, newIndex) {
    const
      idLookup = new RegExp(`${this.formset.options.prefix}-(\\d+|__prefix__)-`)
    const idReplacement = `${this.formset.options.prefix}-${newIndex}-`;
    ['for', 'id', 'name'].forEach((field) => {
      if (element.hasAttribute(field)) {
        element.setAttribute(
          field,
          element.getAttribute(field).replace(idLookup, idReplacement),
        )
      }
    })
  }

  createDeleteButton() {
    const button = document.createElement('button')
    button.innerText = this.formset.options.deleteButtonLabel
    if (this.formset.options.deleteButtonCssClass) {
      button.setAttribute('class', this.formset.options.deleteButtonCssClass)
    }
    return button
  }

  addDeleteButton() {
    const button = (
      this.formset.options.deleteButtonCreator
      || this.createDeleteButton
    ).call(this)

    if (this.formset.options.deleteContainer) {
      this.element.querySelector(
        this.formset.options.deleteContainer,
      ).appendChild(button)
    } else {
      this.element.appendChild(button)
    }

    button.addEventListener('click', this.deleteHandler.bind(this))
  }

  deleteHandler(event) {
    const
      deleteInput = this.element.querySelector('input[type=hidden][id$="-DELETE"]')

    event.preventDefault()

    if (this.formset.options.deleteConfirmText) {
      if (!window.confirm(this.formset.options.deleteConfirmText)) {
        return false
      }
    }

    if (deleteInput) {
      deleteInput.value = 'on'
      this.element.style.display = 'none'
    } else {
      this.formset.removeForm(this)
    }

    this.formset.ensureAddButtonVisibility()

    if (this.formset.options.deleteCallback) {
      this.formset.options.deleteCallback.call(this)
    }

    return true
  }
}

class Formset {
  constructor(element, options) {
    this.element = element
    this.options = { ...DEFAULT_OPTIONS, ...options }

    this.validateOptions()

    this.formTemplate = this.buildFormTemplate()

    this.totalFormsInput = this.element.querySelector(
      `#id_${this.options.prefix}-TOTAL_FORMS`,
    )
    this.maxFormsInput = this.element.querySelector(
      `#id_${this.options.prefix}-MAX_NUM_FORMS`,
    )

    this.initializeForms()

    this.addButton = this.addAddButton()
    this.ensureAddButtonVisibility()
  }

  validateOptions() {
    if (!this.options.prefix) {
      throw new Error('Prefix missing for formset.')
    }
    return true
  }

  getFormElements() {
    return [...this.element.querySelectorAll(this.options.formSelector)]
  }

  initializeForms() {
    this.getFormElements().forEach((form) => {
      const formInstance = new FormsetForm(this, form)
      if (form.style.display !== 'none' && formInstance.hasChildElements) {
        formInstance.addDeleteButton()
      }
    })
  }

  removeForm(form) {
    form.element.remove()
    this.updateFormIndexes()
  }

  updateFormIndexes() {
    this.totalFormsInput.value = this.getFormElements().length
    this.getFormElements().forEach((form, i) => {
      (new FormsetForm(this, form)).updateIndex(i)
    })
  }

  buildFormTemplate() {
    const
      template = this.getFormElements().pop().cloneNode(true)
    const titleElement = template.querySelector('.formset-form-title')
    const deleteElement = template.querySelector('input[type=hidden][id$="-DELETE"]')

    template.removeAttribute('id')
    template.classList.remove('existing')

    if (titleElement) {
      titleElement.innerText = this.options.addTitle
    }

    if (deleteElement) {
      deleteElement.remove()
    }

    template.querySelectorAll(FORM_CHILD_ELEMENT_SELECTOR).forEach((element) => {
      const elementType = element.getAttribute('type')
      if (['checkbox', 'radio'].some((type) => type === elementType)) {
        element.removeAttribute('checked')
      } else {
        element.value = ''
      }
    })

    return template
  }

  addAnotherAllowed() {
    const
      maxFormsValue = parseInt(this.maxFormsInput.getAttribute('value'), 10) || 0
    const totalFormsValue = this.getFormElements().filter(
      (form) => form.style.display !== 'none',
    ).length
    const visible = (maxFormsValue === 0 || (maxFormsValue - totalFormsValue > 0))

    return visible
  }

  ensureAddButtonVisibility() {
    const visible = this.addAnotherAllowed()
    if (visible) {
      this.addButton.style.display = 'inherit'
    } else {
      this.addButton.style.display = 'none'
    }
  }

  createAddButton() {
    const button = document.createElement('button')
    button.innerText = this.options.addButtonLabel
    if (this.options.addButtonCssClass) {
      button.setAttribute('class', this.options.addButtonCssClass)
    }
    return button
  }

  addAddButton() {
    const button = (
      this.options.addButtonCreator
      || this.createAddButton
    ).call(this)

    if (this.options.addContainer) {
      this.element.querySelector(
        this.options.addContainer,
      ).appendChild(button)
    } else {
      this.element.appendChild(button)
    }

    button.addEventListener('click', this.addHandler.bind(this))
    return button
  }

  addHandler(event) {
    if (event) {
      event.preventDefault()
    }

    if (!this.addAnotherAllowed()) {
      return false
    }

    const newForm = new FormsetForm(this, this.formTemplate.cloneNode(true))
    newForm.addDeleteButton()

    this.element.insertBefore(newForm.element, this.getFormElements().pop().nextSibling)
    this.updateFormIndexes()

    this.ensureAddButtonVisibility()

    if (this.options.addCallback) {
      this.options.addCallback.call(this)
    }

    return true
  }
}

class FormsetInitializer {
  constructor(options) {
    document.querySelectorAll(options.selector).forEach(
      (element) => this.initialize(element),
    )
  }

  initialize(element) {
    if (element.hasAttribute('data-formset-no-initialize')) {
      return
    }

    new Formset(element, this.optionsForElement(element))
  }

  optionsForElement(element) {
    const options = {}

    Object.keys(AVAILABLE_DATA_OPTIONS).forEach((key) => {
      const
        dataKey = `data-formset-${AVAILABLE_DATA_OPTIONS[key]}`
      const value = element.getAttribute(dataKey)

      if (value) {
        options[key] = value
      }
    })

    if ('addCallback' in options) {
      options.addCallback = window[options.addCallback]
    }
    if ('deleteCallback' in options) {
      options.deleteCallback = window[options.deleteCallback]
    }

    return options
  }
}

export { Formset, FormsetInitializer }
