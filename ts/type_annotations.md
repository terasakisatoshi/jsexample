---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.8.0
  kernelspec:
    display_name: TypeScript
    language: typescript
    name: tslab
---

```typescript
var age: number = 32;
var name: string = "John";
var isUpdated: boolean = true;
```

```typescript
function display(id: number, name: string){
    console.log("Id = " + id, ", Name =" + name);
}
```

```typescript
var employee : {
    id: number;
    name: string;
}

employee = {
    id: 100,
    name: "Goma",
}
```

```typescript
display(employee.id, employee.name)
```
