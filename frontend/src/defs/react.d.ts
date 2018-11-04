import React from 'react'

declare module 'react' {

	export function useState <T>(intialValue: T): [T, (v: T) => void]

}
