import * as bs from "react-bootstrap";
import React from "react";
import styled from "styled-components";
import {Button, FormControl, MenuItem, Select, Slider, Typography} from '@material-ui/core';
import {makeStyles} from '@material-ui/core/styles';
import {getUserInfoJson} from "../functions/localstorage";

const useStyles = makeStyles((theme) => ({
    button: {
        display: 'block',
        marginTop: theme.spacing(2),
    },
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
}));

const Field = styled.p`
  color: #3C64B1;
  text-align: left;
  float: left;
`;

export default class LifestyleData extends React.Component {
    constructor(props) {
        super(props);
        this.state = getUserInfoJson().preference_lifestyle;
        this.handleChange = this.handleChange.bind(this);
    }

    handleChange(name, value) {
        if(name=="smoking" || name=="use_aircon"){
            if(value==0){
                value=false;
            } else if(value==null){
                value=false;
            } else {
                value=true;
            }
        }
        this.setState({
            ...this.state,
            [name]:value
        })
        this.props.parentCallBack(name,value);
    }


    render() {
        return (
            <bs.Container>
                <h3>Lifestyle Information</h3>
                <br/>
                <Typography id="socialbility-slider_topo">
                    Sociability
                </Typography>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <bs.Col sm={4}><Slider
                        id="socialbility_slider"
                        name="socialbility"
                        defaultValue={this.state.like_social}
                        aria-labelledby="socialbility-slider"
                        step={1}
                        marks
                        min={0}
                        max={10}
                        onChange={(e, value) => this.handleChange("like_social", value)}
                        color="primary"
                    /></bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <Typography id="cleanliness-slider_topo">
                    Cleanliness
                </Typography>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <bs.Col sm={4}><Slider
                        id="cleanliness_slider"
                        defaultValue={this.state.like_clean}
                        aria-labelledby="cleanliness-slider"
                        step={1}
                        marks
                        min={0}
                        max={10}
                        color="primary"
                        onChange={(e, value) => this.handleChange("like_clean", value)}
                    /></bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <Typography id="noisiness-slider">
                    Noisiness Level
                </Typography>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <bs.Col sm={4}><Slider
                        id="noisiness_slider"
                        defaultValue={this.state.like_quiet}
                        aria-labelledby="noisiness-slider"
                        step={1}
                        marks
                        min={0}
                        max={10}
                        valueLabelDisplay="auto"
                        color="primary"
                        onChange={(e, value) => this.handleChange("like_quiet", value)}
                    /></bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <Typography id="aircon-slider">
                    Use Aircon
                </Typography>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <bs.Col sm={4}><Slider
                        id="aircon_slider"
                        defaultValue={this.state.use_aircon ===false ? 0 : this.state.use_aircon === true ? 1: 0}
                        aria-labelledby="aircon-slider"
                        step={1}
                        marks
                        min={0}
                        max={1}
                        valueLabelDisplay="off"
                        color="secondary"
                        onChange={(e, value) => this.handleChange("use_aircon", value)}
                    /></bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <Typography id="smokes-slider">
                    Smokes
                </Typography>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <bs.Col sm={4}><Slider
                        id="smokes_slider"
                        defaultValue={this.state.smoking === false ? 0 : this.state.smoking === true ? 1 : 0}
                        aria-labelledby="smokes-slider"
                        step={1}
                        marks
                        min={0}
                        max={1}
                        valueLabelDisplay="off"
                        color="secondary"
                        onChange={(e, value) => this.handleChange("smoking", value)}
                    /></bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>

                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <Button id="controlDropdownSleep" className={useStyles.button} onClick={()=>{
                        this.setState({
                            sleepDropDownOpen : true
                        })
                    }}>
                        Sleeping Time
                    </Button>
                    <FormControl className={useStyles.formControl}>
                        
                        <Select
                        labelId="demo-controlled-open-select-label"
                        id="selectSleep"
                        open={this.state.sleepDropDownOpen}
                        onClose={()=>{
                            this.setState({
                                sleepDropDownOpen : false
                            })
                        }}
                        onOpen={()=>{ 
                            this.setState({
                                sleepDropDownOpen : true
                            })
                        }}
                        value={this.state.sleep_time}
                        onChange={(e)=> this.handleChange("sleep_time",e.target.value)}
                        >
                        <MenuItem id="sleepMenuItem21" value={21}>21:00</MenuItem>
                        <MenuItem id="sleepMenuItem22" value={22}>22:00</MenuItem>
                        <MenuItem id="sleepMenuItem23" value={23}>23:00</MenuItem>
                        <MenuItem id="sleepMenuItem0" value={0}>00:00</MenuItem>
                        <MenuItem id="sleepMenuItem1" value={1}>1:00</MenuItem>
                        <MenuItem id="sleepMenuItem2" value={2}>2:00</MenuItem>
                        </Select>
                    </FormControl>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <br/>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                    <Button id="controlDropdownWake" className={useStyles.button} onClick={()=>{
                        this.setState({
                            wakeUpDropDownOpen : true
                        })
                    }}>
                        Waking Up Time
                    </Button>
                    <FormControl className={useStyles.formControl}>
                        
                        <Select
                        labelId="demo-controlled-open-select-label"
                        id="selectWake"
                        open={this.state.wakeUpDropDownOpen}
                        onClose={()=>{
                            this.setState({
                                wakeUpDropDownOpen : false
                            })
                        }}
                        onOpen={()=>{ 
                            this.setState({
                                wakeUpDropDownOpen : true
                            })
                        }}
                        value={this.state.wakeup_time}
                        onChange={(e)=> this.handleChange("wakeup_time",e.target.value)}
                        >
                        <MenuItem id="wakeMenuItem5" value={5}>5:00</MenuItem>
                        <MenuItem id="wakeMenuItem6" value={6}>6:00</MenuItem>
                        <MenuItem id="wakeMenuItem7" value={7}>7:00</MenuItem>
                        <MenuItem id="wakeMenuItem8" value={8}>8:00</MenuItem>
                        <MenuItem id="wakeMenuItem9" value={9}>9:00</MenuItem>
                        <MenuItem id="wakeMenuItem10" value={10}>10:00</MenuItem>
                        <MenuItem id="wakeMenuItem11" value={11}>11:00</MenuItem>
                        </Select>
                    </FormControl>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                <br/>
                <bs.Row>
                    <bs.Col sm={4}></bs.Col>
                        <bs.Col>
                            <Field >Diet</Field>
                            <input id="lifestyle_diet" name="diet" placeholder={this.state.diet}
                             onChange={(e)=>this.handleChange("diet",e.target.value)}/>
                        </bs.Col>
                    <bs.Col sm={4}></bs.Col>
                </bs.Row>
                
            </bs.Container>
        );
    }
}
