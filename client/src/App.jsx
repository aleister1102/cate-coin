import useFetch from './hooks/useFetch'
import Header from './components/Header'
import Blockchain from './components/Blockchain'

function App() {
	const blockchain = useFetch(`http://localhost:8080/get-chain`)

	return (
		<>
			<Header></Header>
            <Blockchain blockchain={blockchain}></Blockchain>
		</>
	)
}

export default App
