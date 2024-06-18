# Input Variables:

## tableHeader

```tableHeader``` is an array of strings that contains the table headers 

Example:
```
[tableHeader] = [ 'name', 'type', 'year' ];
```

## tableBody

```tableBody``` array of object that contains the table body 

Example:
```
[tableBody] = [ 
    {
        name: '12345',
        type: 'IFN',
        year: '1993'
    },
    {
        name: '67890',
        type: 'Por parcelas',
        year: '2003'
    }
];
```

## tableTitle

```tableTitle``` string with the name of the view. It has to be the same that in translations

Example:
```
[tableTitle]="'scenarios'"
```
Note: scenarios is the key in translations files

## rowButtons

```rowButtons``` array with the actions that you want to show in the table. It can be: 
- results
- details
- edit
- delete

Example:
```
[rowButtons]="['results','details', 'delete']"
```
Note: scenarios is the key in translations files
