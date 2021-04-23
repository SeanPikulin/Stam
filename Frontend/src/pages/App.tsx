import React from 'react';
import { BrowserRouter, Switch, Route } from 'react-router-dom';

import Home from './Home';
import Cart from './Cart';
import Navbar from './Navbar';
import SignIn from './SignIn';
import SignUp from './SignUp';

function App() {
	return (
		<>
			<BrowserRouter>
				<Navbar />
				<Switch>
					<Route path="/" exact component={Cart} />
					<Route path="/cart" exact component={Home} />
					<Route path="/sign-in" exact component={SignIn} />
					<Route path="/sign-up" exact component={SignUp} />
				</Switch>
			</BrowserRouter>
		</>
	);
}

export default App;
