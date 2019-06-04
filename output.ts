export interface Foo {
	some_field: string;
	another_field: number;
}

export interface Bar {
	foo: Foo;
	foos: Foo[];
	bar_field: Date;
}

