import React, { FC } from 'react';

import { ListItem, ListItemSecondaryAction, ListItemText } from '@material-ui/core';
import DeleteForeverOutlinedIcon from '@material-ui/icons/DeleteForeverOutlined';
import EditIcon from '@material-ui/icons/Edit';

import useAPI from '../../hooks/useAPI';
import { ProductQuantity } from '../../types';
import ProductDetails from '../DetailsWindows/ProductDetails';
import ProductForm from '../FormWindows/ProductForm';
import GenericList from './GenericList';
import SecondaryActionButton from './SecondaryActionButton';
import { areYouSure, confirmOnSuccess } from '../../decorators';

type ProductsListProps = {
	products: ProductQuantity[];
	setProducts: (newProducts: ProductQuantity[]) => void;
	openTab: (component: FC, selectedItem: string) => void;
	selectedItem: string;
	storeId: string;
};

const ProductsList: FC<ProductsListProps> = ({
	products,
	openTab,
	selectedItem,
	setProducts,
	storeId,
}) => {
	const createProduct = useAPI<string>('/create_product', {}, 'POST');

	const deleteProductAPI = useAPI<null>(
		'/remove_product_from_store',
		{ store_id: storeId },
		'POST'
	);
	const editProductAPI = useAPI<null>('/edit_product_details', { store_id: storeId }, 'POST');
	const editProductQuantityAPI = useAPI<null>(
		'/change_product_quantity',
		{ store_id: storeId },
		'POST'
	);

	const handleCreateProduct = (
		name: string,
		price: number,
		quantity: number,
		category: string,
		keywords: string[]
	) => {
		createProduct
			.request({
				store_id: storeId,
				name,
				price,
				quantity,
				category,
				keywords,
			})
			.then((createProduct) => {
				if (!createProduct.error && createProduct.data !== null) {
					setProducts([
						{
							id: createProduct.data.data,
							name,
							price,
							category,
							keywords,
							quantity,
						},
						...products,
					]);
				}
			});
	};
	const handleEditProduct = confirmOnSuccess(
		(
			id: string,
			name: string,
			price: number,
			quantity: number,
			category: string,
			keywords: string[]
		) => {
			return editProductAPI
				.request({
					product_id: id,
					store_id: storeId,
					new_name: name,
					new_price: price,
					new_category: category,
					keywords: keywords,
				})
				.then((createProduct) => {
					if (!createProduct.error && createProduct.data !== null) {
						setProducts(
							products.map((product) =>
								product.id === id
									? {
											id,
											category,
											keywords,
											name,
											price,
											quantity: product.quantity,
									  }
									: product
							)
						);
					}
					return editProductQuantityAPI
						.request({
							product_id: id,
							quantity,
						})
						.then((editProduct) => {
							if (!editProduct.error && editProduct.data !== null) {
								setProducts(
									products.map((product) =>
										product.id === id
											? {
													id,
													category,
													keywords,
													name,
													price,
													quantity,
											  }
											: product
									)
								);
								return true;
							}
							return false;
						});
				});
		},
		'Edited!',
		'The product was edited successfully!'
	);

	const openProductForm = (productToEdit: ProductQuantity | undefined = undefined) => {
		openTab(
			() => (
				<ProductForm
					onSubmit={
						productToEdit
							? (name, price, quantity, category, keywords) =>
									handleEditProduct(
										productToEdit.id,
										name,
										price,
										quantity,
										category,
										keywords
									)
							: handleCreateProduct
					}
					productEditing={productToEdit}
				/>
			),
			''
		);
	};

	const onSelectProduct = (product: ProductQuantity) => {
		if (product.id !== selectedItem) {
			openTab(() => <ProductDetails product={product} />, product.id);
		}
	};

	const onDelete = areYouSure(
		(productId: string) => {
			deleteProductAPI.request({ product_id: productId }, (data, error) => {
				if (!error && data !== null) {
					setProducts(products.filter((product) => product.id !== productId));
				}
			});
		},
		"You won't be able to revert this!",
		'Yes, delete product!'
	);

	return (
		<GenericList
			data={products}
			onCreate={() => openProductForm()}
			header="Products"
			createTxt="+ Add a new product"
			narrow
		>
			{(product: ProductQuantity) => (
				<ListItem
					key={product.id}
					selected={selectedItem === product.id}
					onClick={() => onSelectProduct(product)}
					button
				>
					<ListItemText primary={product.name} className="first-field" />
					<ListItemText primary={`in stock: ${product.quantity}`} />
					<ListItemSecondaryAction>
						<SecondaryActionButton onClick={() => openProductForm(product)}>
							<EditIcon />
						</SecondaryActionButton>
						<SecondaryActionButton onClick={() => onDelete(product.id)}>
							<DeleteForeverOutlinedIcon />
						</SecondaryActionButton>
					</ListItemSecondaryAction>
				</ListItem>
			)}
		</GenericList>
	);
};

export default ProductsList;
