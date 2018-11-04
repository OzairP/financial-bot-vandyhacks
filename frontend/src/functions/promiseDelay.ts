import delay from 'delay'

export const promiseDelay = <T>(promise: Promise<T>, ms: number, opts?: {
	delayRejection: boolean
}): Promise<T> => {
	opts = Object.assign({
		delayRejection: true
	}, opts)

	let promiseErr: Promise<any>

	if (opts.delayRejection) {
		promise = promise.catch(err => {
			promiseErr = err
		}) as any
	}

	return Promise.all([promise, delay(ms)])
		.then(val => promiseErr ? Promise.reject(promiseErr) : val[0] as any)
}
