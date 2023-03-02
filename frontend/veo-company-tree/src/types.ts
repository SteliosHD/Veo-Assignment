export type TreeSelectedProps = {
  id: number
  name: string
}

export type TreeType = {
  name: string
  id: number
  parent_id_id: number
  sub_tree: TreeType[]
}

export type TreeResponseData = {
  tree: string
  url: string
  message: string
}

export type TreeErrorResponse = {
  message: string
}
