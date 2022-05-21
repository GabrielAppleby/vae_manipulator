import {createAsyncThunk, createSlice} from '@reduxjs/toolkit';
import {RootState} from '../app/store';
import {API_URL} from "../env";

type Status = 'idle' | 'pending' | 'fulfilled' | 'rejected';

interface ProductState {
    product?: string;
    productStatus: Status;
}

const initialState: ProductState = {
    product: undefined,
    productStatus: 'idle'
}


export const fetchProduct = createAsyncThunk<any, void, { state: RootState }>('product/fetchProduct', async (arg, thunkAPI) => {
    const url = new URL(`${API_URL}api/model/encode`);
    const state = thunkAPI.getState();
    const entities = state.selection.entities;
    const values = Object.values(entities);
    // @ts-ignore
    const sp = [['url1', values[0].url]]
    if (values.length > 2)
    {
        // @ts-ignore
        sp.push(['url2', values[1].url])
        // @ts-ignore
        sp.push(['url3', values[2].url])
    }
    // @ts-ignore
    url.search = new URLSearchParams(sp).toString();
    const request = new Request(url.toString());
    const response = await fetch(request, {method: 'POST'});
    if (!response.ok) {
        throw new Error(response.statusText);
    }
    return response.blob().then((blob) => {
        return URL.createObjectURL(blob)
    }).catch(() => ({}));
})

export const productSlice = createSlice({
    name: 'product',
    initialState,
    reducers: {},
    extraReducers: builder => {
        builder.addCase(fetchProduct.pending, (state) => {
            state.productStatus = 'pending'
        })
        builder.addCase(fetchProduct.fulfilled, (state, action) => {
            state.productStatus = 'fulfilled'
            // @ts-ignore
            state.product = action.payload;
        })
        builder.addCase(fetchProduct.rejected, (state) => {
            state.productStatus = 'rejected'
        })
    }
});


export const selectProduct = (state: RootState) => {
    return state.product.product;
}

export default productSlice.reducer;
