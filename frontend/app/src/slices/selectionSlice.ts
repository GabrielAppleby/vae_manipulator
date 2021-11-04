import {createEntityAdapter, createSlice} from '@reduxjs/toolkit';
import {OCT} from "../services/oct";
import {RootState} from "../app/store";


const selectionAdapter = createEntityAdapter<OCT>({
    selectId: instance => instance.uid
});


export const selectionSlice = createSlice({
    name: 'selection',
    initialState: selectionAdapter.getInitialState(),
    reducers: {
        selectionAdded(state, action) {
            if (state.ids.length > 1) {
                selectionAdapter.removeOne(state, state.ids[0])
                selectionAdapter.addOne(state, action.payload);
            }
            selectionAdapter.addOne(state, action.payload);
        }
    }
});

export const {selectionAdded} = selectionSlice.actions;

export const {selectAll} = selectionAdapter.getSelectors<RootState>(state => state.selection);

export default selectionSlice.reducer;
