import React from "react";
import {connect, ConnectedProps} from "react-redux";
import {RootState} from "../app/store";
import {API_URL} from "../env";
import {selectAll} from "../slices/selectionSlice";
import {ImageList, ImageListItem, Typography} from "@material-ui/core";
import {makeStyles} from "@material-ui/core/styles";


const mapStateToProps = (state: RootState) => ({
    selectedInstances: selectAll(state),
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



const DefaultImageList = (props: PropsFromRedux) => {
    const images = Array.from(props.selectedInstances);
    const classes = useStyles();

    return (
        <ImageList rowHeight={'auto'} cols={5} className={classes.list}>
            {images.map((item) => (
                <ImageListItem key={item.url} style={{width: 84, height:84}}>
                    <div>
                        <img src={API_URL + `images/${item.url}`} style={{width: 64, height:64}}/>
                    </div>
                    <div>
                        <Typography variant="body1">
                            {item.label}
                        </Typography>
                    </div>
                </ImageListItem>
            ))}
        </ImageList>
        // <>
        //     {images.map((item) => (
        //         <div key={item.url}>
        //             <img src={API_URL + `images/${item.url}`} width="32" height="32"/>
        //         </div>
        //     ))}
        // </>
    );
}

export default connector(DefaultImageList);
