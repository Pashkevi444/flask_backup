const grid = document.querySelector('revo-grid');
const columns = [
  {
      prop: 'name',
      name: 'First',
      sortable: true,
      order: 'asc'
  },
  {
      prop: 'details',
      name: 'Second',
      sortable: true,
      order: 'asc'
  }
];
const rows = [{
  name: 'New item',
  details: 'Item description'
},
{
  name: '2New item',
  details: '2Item description'
}
];

grid.columns = columns;
grid.source = rows;