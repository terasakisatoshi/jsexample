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
interface IEmployee {
    empCode: number;
    empName: string;
    getSalary: (number) => number; // arrwo function
    getManagerName(number): string;
}
```

```typescript
interface KeyPair {
    key: number;
    value: string;
}
```

```typescript
let kv1: KeyPair = {key:1, value:"Steve"};
```

```typescript
interface KeyValueProcessor{
    (key: number, value: string): void;
}

function addKeyValue(key:number, value:string):void {
    console.log("addKeyValue: key = " + key + ", value = " + value);
}

let kvp:KeyValueProcessor = Math.sin // この時点でコンパイラーエラにならない
```

```typescript
kvp(Math.PI)
```

```typescript
interface IEmployee {
    empCode: number;
    name: string;
    getSalary:(number) => number;
}

class Employee implements IEmployee {
    empCode: number;
    name: string;
    
    constructor(code: number, name: string){
        this.empCode = code;
        this.name = name;
    }
    
    getSalary(empCode: number): number {
        return 2000;
    }
}
```

```typescript
let emp = new Employee(1, "Steve");
```

```typescript
emp.name
```

```typescript
emp.empCode
```

```typescript
emp.getSalary(10)
```
