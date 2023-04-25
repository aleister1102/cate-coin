import useFetch from './hooks/useFetch'
import Header from './components/Header'
import Blockchain from './components/Blockchain'
import AddTransactionsForm from './components/AddTransactionsForm'
import MineBlock from './components/MineBlock'
import TransactionsQueue from './components/TransactionsQueue'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'


function App() {
	const blockchain = useFetch(`http://localhost:8080/get-chain`)

	return (
		<Router>
			<Header/>
            <Routes>    
                <Route path="/" element={<Blockchain blockchain={blockchain}/>} />
                <Route path='/add-transactions' element={<AddTransactionsForm/>} />
                <Route path='/transactions-queue' element={<TransactionsQueue blockchain={blockchain}/>} />
                <Route path='/mine-block' element={<MineBlock/>} />
            </Routes>   
		</Router>
	)
}

export default App
