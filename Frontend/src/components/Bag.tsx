
import { Button} from '@material-ui/core';
import React ,{FC, useEffect, useState} from 'react';
import CartProduct from '../components/CartProduct';
import PurchaseIcon from '@material-ui/icons/LocalMall';
import { Link } from 'react-router-dom';
import '../styles/Bag.scss';

type BagProps = {
    storeName:string,
    products:{id:string, name:string,price:number,quantity:number}[],
    propHandleDelete:(product:{id:string,name:string,price:number})=>void,
   
};
type Product = {
	id:string,
    name:string,
    price: number,
    quantity:number
}
const Bag: FC<BagProps> = ({storeName,products,propHandleDelete}:BagProps) => {

    const [productsInCart,setProducts] = useState<{id:string,name:string,price:number,quantity:number}[]>(products);

    useEffect(()=>{
        setProducts(products);
    },[products]);

	const calculateTotal = ()=>{
		const reducer = (accumulator:number, currentValue:Product) => accumulator + (currentValue.price*currentValue.quantity);
		return productsInCart.reduce(reducer,0);
	}
	const [total,setTotal] = useState<number>(calculateTotal());

	const onRemove = (id: string) => {
		setProducts(productsInCart.filter((product) => product.id !== id));
	}
    const onChangeQuantity = (id: string, newQuantity: number) => {
		productsInCart.forEach((product) => {
			if (product.id === id) {
				product.quantity = newQuantity;
				if(newQuantity===0){
					onRemove(id);
				}
			}
		});
		setTotal(calculateTotal());
	}
	
    return (
		
		<div className="page">
			<div className="order-cont">
				<div className="products-cont">
					<h4>{storeName}</h4>
					<span className="line" />
					{productsInCart.length !== 0 ? (
						productsInCart.map((product) => (
							<CartProduct
								key={product.id}
								product={product}
								onRemove={onRemove}
								onChangeQuantity={onChangeQuantity}
							/>
						))
					) : (
						<>
							<h4 className="empty-bag-msg">Your bag is empty</h4>
							<h5>
								You can find products to purchase at the <Link to="/">store</Link>{' '}
							</h5>
						</>
					)}
				</div>
				<div className="summary-cont">
					<h4>Order Summary</h4>
					<span className="line" />
					<div className="total-price">
						<h4>Total:</h4>
						<h4>{total}$</h4>
					</div>
					{/* <Button variant="contained" color="secondary" startIcon={<PurchaseIcon />}>
						Checkout
					</Button> */}
				</div>
			</div>
		</div>
	);
}

export default Bag;
