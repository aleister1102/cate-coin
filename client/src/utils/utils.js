export const capitalizeString = (string) =>
	string.charAt(0).toUpperCase() + string.slice(1)

export const parseTransactionString = (transactionString) => {
	// Use regex to match the sender, receiver, amount, and change values
	const regex = /([a-zA-Z]+) -> ([a-zA-Z]+): (\d+), change: (\d+)/
	const match = transactionString.match(regex)

	// Extract the matched values into separate variables
	const sender = match[1]
	const receiver = match[2]
	const amount = match[3]
	const change = match[4]

	return {
		sender,
		receiver,
		amount,
		change,
	}
}
