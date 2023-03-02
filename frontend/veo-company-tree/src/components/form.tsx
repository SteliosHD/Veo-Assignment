import { useState } from 'react'
import { useMutation } from 'react-query'
import { TreeSelectedProps } from '../types'
import { FormValues, FormRequestData, FormSuccessResponse, FormErrorResponse } from './types'
import '../static/form.css'
import { API_URL } from '../utils'

const handleSuccess = (res: Response) => {
  const resPromise = res.json()
  resPromise.then((successData) => {
    alert(successData.message)
  })
  return resPromise
}

export default function Form({ selected }: { selected: TreeSelectedProps }) {
  const nodeTypes = ['Manager', 'Developer', 'Employee']

  const [formValues, setFormValues] = useState<FormValues>({
    name: '',
    nodeType: 'Employee',
    department: undefined,
    languagePreference: undefined,
  })

  const { mutate } = useMutation<FormSuccessResponse, FormErrorResponse, FormRequestData>(
    (newNode) =>
      fetch(API_URL + 'nodes/' + selected.id, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newNode),
      })
        .then(handleSuccess)
        .catch((err) => console.log(err.then((errData: FormErrorResponse) => errData.message))),
  )

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = event.target

    if (name === 'nodeType') {
      if (value === 'Manager') {
        setFormValues({ ...formValues, nodeType: value, department: '' })
      } else if (value === 'Developer') {
        setFormValues({
          ...formValues,
          nodeType: value,
          languagePreference: '',
        })
      } else {
        setFormValues({ ...formValues, nodeType: value })
      }
    } else {
      setFormValues({ ...formValues, [name]: value })
    }
  }


  const prepareRequestData = (): FormRequestData => {
    const requestData: FormRequestData = {
      name: formValues.name,
      node_type: formValues.nodeType.toUpperCase(),
      parent_id: selected.id,
    }

    if (formValues.nodeType === 'Manager' && formValues.department) {
      requestData['department_name'] = formValues.department
    } else if (formValues.nodeType === 'Developer' && formValues.languagePreference) {
      requestData['language_preference'] = formValues.languagePreference
    }
    return requestData
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    mutate(prepareRequestData())
  }

  return (
    <form onSubmit={handleSubmit}>
      <div className='mb-3'>
        <label className='form-label'>
          Child node name:
          <input
            className='form-control'
            type='text'
            name='name'
            value={formValues.name}
            onChange={handleInputChange}
            required
          />
        </label>
      </div>
      <div className='mb-3'>
        <label className='form-label'>
          Child node type:
          <select
            className='form-select'
            name='nodeType'
            value={formValues.nodeType}
            onChange={handleInputChange}
            required
          >
            <option value=''>Select a type</option>
            {nodeTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>
      </div>

      <div className='mb-3'>
        {formValues.nodeType === 'Manager' && (
          <label className='form-label'>
            Child node department:
            <input
              className='form-control'
              type='text'
              name='department'
              value={formValues.department || ''}
              onChange={handleInputChange}
            />
          </label>
        )}

        {formValues.nodeType === 'Developer' && (
          <label className='form-label'>
            Child node language preference:
            <input
              className='form-control'
              type='text'
              name='languagePreference'
              value={formValues.languagePreference || ''}
              onChange={handleInputChange}
            />
          </label>
        )}
      </div>
      <button
        className='btn btn-primary'
        type='submit'
        disabled={selected.id === -1 ? true : false}
      >
        Submit
      </button>
      {selected.id === -1 && (
        <span className='span-warn'>Select a parent node to create a new node</span>
      )}
    </form>
  )
}
