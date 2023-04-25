import { useEffect, useState } from 'react'
import Block from './Block'

export default function Blockchain({ blockchain }) {
	const [chain, setChain] = useState([])
	let blocks = []

	useEffect(() => {
		setChain(blockchain.chain)
	}, [blockchain])

	if (chain) {
		blocks = chain.map((block) => <Block block={block}></Block>)
	}

	return (
		<ul className='flex justify-center items-center gap-16 w-full mt-8'>
			{blocks.map((block, index) => (
				<li key={index}>{block}</li>
			))}
		</ul>
	)
}
