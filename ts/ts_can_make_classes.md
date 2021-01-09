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
class Employee {
    empCode: number;
    empName: string;
    
    constructor(code: number, name: string) {
        this.empName = name;
        this.empCode = code;
    }
    
    getSalary(): number {
        return 100;
    }
}
```

```typescript
let emp = new Employee(100, "Goma");
```

```typescript
class Point{
    x: number;
    y: number;
}

let p = new Point()
```

```typescript
p.x = 1
p.y = 3

p
```

```typescript
class Person{
    name: string;
    
    constructor(name: string){
        this.name = name;
    }
}

class Employee extends Person {
    empCode: number;
    
    constructor(empCode: number, name:string){
        super(name);
        this.empCode = empCode;
    }
    
    displayName(): void{
        console.log("Name = " + this.name + ", Employee Code = " + this.empCode);
    }
}

let emp = new Employee(100, "Bill");
emp.displayName();
```
