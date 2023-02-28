const tree_json = {
  trees: [
    {
      id: 1,
      name: "CEO",
      parent_id_id: 0,
      sub_tree: [
        {
          id: 2,
          name: "CFO",
          parent_id_id: 1,
          sub_tree: [
            {
              id: 11,
              name: "Sara",
              parent_id_id: 2,
              sub_tree: [
                {
                  id: 14,
                  name: "Suzanne",
                  parent_id_id: 11,
                  sub_tree: [],
                },
              ],
            },
          ],
        },
        {
          id: 3,
          name: "CTO",
          parent_id_id: 1,
          sub_tree: [
            {
              id: 5,
              name: "Daniel",
              parent_id_id: 3,
              sub_tree: [],
            },
            {
              id: 6,
              name: "Mark",
              parent_id_id: 3,
              sub_tree: [],
            },
            {
              id: 7,
              name: "John",
              parent_id_id: 3,
              sub_tree: [],
            },
            {
              id: 8,
              name: "Peter",
              parent_id_id: 3,
              sub_tree: [],
            },
            {
              id: 9,
              name: "Mary",
              parent_id_id: 3,
              sub_tree: [],
            },
            {
              id: 10,
              name: "Jane",
              parent_id_id: 3,
              sub_tree: [],
            },
          ],
        },
        {
          id: 4,
          name: "CPO",
          parent_id_id: 1,
          sub_tree: [
            {
              id: 12,
              name: "Sally",
              parent_id_id: 4,
              sub_tree: [],
            },
            {
              id: 13,
              name: "Samantha",
              parent_id_id: 4,
              sub_tree: [],
            },
          ],
        },
      ],
    },
  ],
};

export default tree_json;