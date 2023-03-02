import { TreeSelectedProps, TreeType, TreeResponseData, TreeErrorResponse } from './types'
import { tree_json as TreeJSON } from './Data/tree_outputs'
import './static/App.css'
import Tree from './components/tree'
import Form from './components/form'
import { useState } from 'react'
import { useQuery } from 'react-query'
import { API_URL } from './utils'

const getData = (data: TreeResponseData | undefined) => {
  if (process.env.DEBUG === 'true') {
    return TreeJSON.trees[0]
  } else {
    return JSON.parse(data?.tree as string)
  }
}

export default function App() {
  const [selected, setSelected] = useState<TreeSelectedProps>({ id: -1, name: 'None' })
  const { isLoading, error, data } = useQuery<boolean, TreeErrorResponse, TreeResponseData>(
    'tree',
    () => fetch(API_URL + 'tree').then((res) => res.json()),
  )

  if (isLoading) {
    return (
      <div className='d-flex align-items-center m-5'>
        <strong>Loading...</strong>
        <div className='spinner-border ms-auto text-info' role='status' aria-hidden='true'></div>
      </div>
    )
  }

  if (error) {
    return <div>An error occurred: {error.message}</div>
  }

  const treeJSON = getData(data) as TreeType

  return (
    <>
      <nav className='navbar navbar-light'>
        <div className='container'>
          <a className='navbar-brand' href='/'>
            <img src={process.env.PUBLIC_URL + '/logo.png'} alt='' width='50' /> Veo Assignment
          </a>
        </div>
      </nav>
      <div className='App container'>
        <div className='row'>
          <div className='col-6'>
            <h1>Company Structure</h1>
            {treeJSON.sub_tree && (
              <Tree data={treeJSON} selectedState={{ selected, setSelected }} />
            )}
          </div>
          <div className='wrapper col-6'>
            <h2>Create a child node</h2>
            <div className='selected-wrapper'>
              <h5 className='selected-wrapper--text'>
                Selected Parent Node:{' '}
                <span className='selected-wrapper--node'>
                  {selected.id !== -1 ? selected.name : 'None'}
                </span>
              </h5>
            </div>
            <Form selected={selected} />
          </div>
        </div>
      </div>
    </>
  )
}
