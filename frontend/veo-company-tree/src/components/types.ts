export type FormValues = {
  name: string
  nodeType: string
  department?: string
  languagePreference?: string
}

export type FormRequestData = {
  name: string
  node_type: string
  parent_id: number
  department_name?: string
  language_preference?: string
}

export type FormSuccessResponse = {
  message: string
  url: string
}

export type FormErrorResponse = {
    error: string
    message: string
}