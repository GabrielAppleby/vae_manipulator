import React from "react";
import {connect, ConnectedProps} from "react-redux";
import {AppDispatch, RootState} from "../app/store";
import {API_URL} from "../env";
import {selectAll} from "../slices/selectionSlice";
import {ImageList, ImageListItem, Typography} from "@material-ui/core";
import {makeStyles} from "@material-ui/core/styles";
import {fetchProduct, selectProduct} from "../slices/productSlice";


const mapStateToProps = (state: RootState) => ({
    product: selectProduct(state),
});


const connector = connect(
    mapStateToProps,
);

type PropsFromRedux = ConnectedProps<typeof connector>

const useStyles = makeStyles({
    list: {
        alignContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        margin: 'auto',
    },
    item: {
        height: 512,
        width: 512,
    }
});



const Temp = (props: PropsFromRedux) => {
    const product = props.product;
    const classes = useStyles();
    if (product !== undefined)
    {
        console.log(product);
        return (
            <div>
                <img src={product} style={{width: 64, height:64}}/>
            </div>
        );
    }
    return <div></div>


}

export default connector(Temp);
