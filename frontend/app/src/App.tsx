import * as React from 'react'
import ResponsiveScatterChart from "./components/ScatterChart";
import {makeStyles} from "@material-ui/core/styles";
import {DefaultAppBar} from "./components/DefaultAppBar";
import {Grid, ImageList, ImageListItem, Typography} from "@material-ui/core";
import DefaultImageList from "./components/DefaultImageList";
import Temp from "./components/Temp";

const useStyles = makeStyles({
    app: {
        height: '100vh',
        display: 'flex',
        flexDirection: 'column',
    },
    mainGrid: {
        // borderColor: 'blue',
        // borderStyle: 'solid'
    },
    leftPanel: {
        // borderColor: 'orange',
        // borderStyle: 'solid'
    },
    rightPanel: {
        // borderColor: 'yellow',
        // borderStyle: 'solid'
        alignContent: 'center',
        alignItems: 'center',
        textAlign: 'center',
        margin: 'auto'
    },
});

export default function App() {
    const classes = useStyles();

    return (
        <div className={classes.app}>
            <DefaultAppBar organizationName={"VALT"} appName={"Embedding Combiner"}/>
            <Grid container item className={classes.mainGrid}>
                <Grid item xs={12} md={8} className={classes.leftPanel}>
                    <ResponsiveScatterChart/>
                </Grid>
                <Grid container item direction={'column'} xs={12} md={4} className={classes.rightPanel}>
                    <Grid item xs={10} className={classes.rightPanel}>
                        <DefaultImageList/>
                    </Grid>
                    <Grid item xs={10} className={classes.rightPanel}>
                        <Temp></Temp>
                    </Grid>
                </Grid>
            </Grid>
        </div>
  )
}
