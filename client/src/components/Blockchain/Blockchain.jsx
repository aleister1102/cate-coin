import { useEffect, useState } from 'react'
import Block from './Block'
import { IoLink } from 'react-icons/io5'

export default function Blockchain({ blockchain }) {
	const [chain, setChain] = useState()
	

	useEffect(() => {
		setChain(blockchain.chain)
	}, [blockchain])

	const blocks = chain
		? chain.flatMap((block, index) => [
				<Block
					key={block.index}
					block={block}
				/>,
				index !== chain.length - 1 ? <IoLink key={index} /> : null,
        ])
		: []

	return (
		<ul className='flex flex-wrap justify-center items-center mt-36 mb-12 px-16 w-full gap-y-8'>
			{blocks.map((block, index) => (
				<li key={index}> {block} </li>
			))}
		</ul>
	)
}
