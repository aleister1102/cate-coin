import { useState } from 'react'
import { CopyToClipboard } from 'react-copy-to-clipboard'
import classNames from 'classnames'

export default function CopyButton({ text }) {
	const [copied, setCopied] = useState(false)

	const handleCopy = () => {
		setCopied(true)
		setTimeout(() => {
			setCopied(false)
		}, 2000)
	}

	return (
		<CopyToClipboard
			text={text}
			onCopy={handleCopy}>
			<button
				className={classNames(
					'bg-primary hover:bg-pink-600 text-white font-bold py-1 px-4 rounded w-40',
					{ 'bg-pink-600': copied },
				)}
				type='button'>
				{copied ? 'Copied!' : 'Copy hash'}
			</button>
		</CopyToClipboard>
	)
}
